#!/usr/bin/env python3
"""Validate course-poster workflow evidence; never replace visual review."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys


def image_size(path):
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n' and len(data) >= 24:
        return list(struct.unpack('>II', data[16:24]))
    if data[:2] == b'\xff\xd8':
        pos = 2
        while pos + 3 < len(data):
            if data[pos] != 255:
                pos += 1
                continue
            while pos < len(data) and data[pos] == 255:
                pos += 1
            if pos >= len(data):
                break
            marker = data[pos]
            pos += 1
            if marker in (0xD8, 0xD9) or 0xD0 <= marker <= 0xD7:
                continue
            if marker == 0xDA:
                break
            if pos + 2 > len(data):
                break
            length = struct.unpack('>H', data[pos:pos + 2])[0]
            if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                          0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF) and pos + 7 <= len(data):
                height, width = struct.unpack('>HH', data[pos + 3:pos + 7])
                return [width, height]
            if length < 2:
                break
            pos += length
    raise ValueError('仅支持有效PNG/JPEG的像素读取；其他格式需先用可信工具核验')


def validate(record, root, stage):
    errors = []

    def need(condition, message):
        if not condition:
            errors.append(message)

    def file_exists(value, label, sha=None):
        if not isinstance(value, str) or not value:
            errors.append(label + ': 缺少文件路径')
            return None
        path = root / value
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(label + ': 文件不存在或为空')
            return None
        if sha is not None:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            need(actual == sha, label + ': SHA256不一致')
        return path

    need(record.get('schema_version') == 1, '记录格式版本错误')
    outline = record.get('has_outline')
    need(type(outline) is bool, '必须明确有无大纲')
    need(record.get('facts_confirmed') is True, '关键事实未确认')
    sources = record.get('source_files', [])
    need(bool(sources), '缺少真实资料来源')
    for source in sources:
        file_exists(source.get('path'), '来源', source.get('sha256', ''))
    items = record.get('items', [])
    ids = [item.get('id') for item in items]
    need(bool(items), '文案清单为空')
    need(all(ids) and len(set(ids)) == len(ids), '文案ID缺失或重复')
    for item in items:
        label = str(item.get('id', '?'))
        need(bool(item.get('text')) and bool(item.get('source')), label + ': 原文或来源缺失')
        page = item.get('page')
        kind = item.get('kind')
        if outline is True:
            if kind == 'outline':
                need(page == 2, label + ': 大纲必须在第2张')
            elif kind not in ('title', 'navigation'):
                need(page == 1, label + ': 非大纲信息必须在第1张')
            need(page in (1, 2), label + ': 页码错误')
        elif outline is False:
            need(page == 1, label + ': 无大纲只能第1张')
            need(kind != 'outline', label + ': 无大纲记录中出现大纲项')
    if outline is True:
        need(any(i.get('kind') == 'outline' for i in items), '有大纲但清单没有大纲小点')
    tool = record.get('tool', {})
    need(tool.get('native') is True, '默认路线必须使用原生生图')
    need(bool(tool.get('entry')) and bool(tool.get('verified_at')), '原生能力入口或核验日期缺失')
    file_exists(tool.get('evidence'), '原生能力证据')
    canvas = record.get('canvas', {})
    need(bool(canvas.get('requested_ratio')) and bool(canvas.get('rationale')), '画布方案或理由缺失')
    nodes = record.get('nodes', {})
    limit = 6 if stage == 'plan' else 12
    for index in range(1, limit + 1):
        key = 'P%02d' % index
        node = nodes.get(key, {})
        if key == 'P10' and outline is False:
            need(node.get('status') == 'not_applicable' and bool(node.get('reason')),
                 '单图P10须标注不适用及理由')
            continue
        need(node.get('status') == 'passed', key + ': 核心节点尚未通过')
        evidence = node.get('evidence', [])
        need(bool(evidence), key + ': 缺少证据')
        for value in evidence:
            file_exists(value, key + '证据')
    if stage == 'plan':
        return errors
    need(not record.get('open_issues'), '仍有未解决问题')
    pages = record.get('pages', [])
    expected = 2 if outline is True else 1
    need(len(pages) == expected, '最终图片数量错误')
    need({p.get('page') for p in pages} == set(range(1, expected + 1)), '最终图片页码缺失或重复')
    observed = collections.Counter()
    sizes = []
    for page in pages:
        number = page.get('page')
        label = '第%s张' % number
        path = file_exists(page.get('file'), label + '原图', page.get('sha256', ''))
        if path:
            try:
                size = image_size(path)
                need(size == page.get('actual_size'), label + ': 实际像素与记录不一致')
                sizes.append(size)
            except (ValueError, struct.error) as exc:
                errors.append(label + ': ' + str(exc))
        for field in ('prompt_file', 'call_evidence', 'review_file'):
            file_exists(page.get(field), label + field)
        need(page.get('visual_review') == 'passed', label + ': 目视未通过')
        for item_id in page.get('observed_items', []):
            observed[item_id] += 1
            matches = [i for i in items if i.get('id') == item_id]
            need(bool(matches), label + ': 出现未知文案ID')
            if matches:
                need(matches[0].get('page') == number, label + ': 观察文案分配错误')
    if expected == 2 and canvas.get('same_size', True):
        need(len(sizes) == 2 and sizes[0] == sizes[1], '双图实际尺寸不一致')
    for item in items:
        count = observed[item.get('id')]
        need(count >= 1, str(item.get('id')) + ': 未在成图核实')
        if item.get('only_once'):
            need(count == 1, str(item.get('id')) + ': 只出现一次的文案重复')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--stage', choices=('plan', 'final'), default='final')
    args = parser.parse_args()
    try:
        data = json.loads(args.record.read_text(encoding='utf-8'))
        errors = validate(data, args.record.resolve().parent, args.stage)
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(json.dumps({'passed': False, 'errors': ['无法读取有效记录: ' + str(exc)]}, ensure_ascii=False))
        return 1
    print(json.dumps({'passed': not errors, 'stage': args.stage, 'errors': errors,
                      'scope': '仅验证结构与证据完整性；不替代真实调用、逐字与目视验收'}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
