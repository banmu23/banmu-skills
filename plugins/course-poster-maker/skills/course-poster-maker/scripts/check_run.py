#!/usr/bin/env python3
"""Check V2 workflow evidence, mappings and file integrity, not visual truth."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct


def image_size(path):
    data = path.read_bytes()
    if data[:8] == b'\x89PNG\r\n\x1a\n' and len(data) >= 24:
        width, height = struct.unpack('>II', data[16:24])
        if width > 0 and height > 0:
            return [width, height]
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
                if width > 0 and height > 0:
                    return [width, height]
            if length < 2:
                break
            pos += length
    raise ValueError('仅支持PNG/JPEG的像素头读取；此检查不能证明图像完整解码或视觉质量')


def validate(record, root, stage):
    errors = []
    root = Path(root)

    def need(condition, message):
        if not condition:
            errors.append(message)

    def obj(value, label):
        if not isinstance(value, dict):
            errors.append(label + ': 必须为对象')
            return {}
        return value

    def arr(value, label):
        if not isinstance(value, list):
            errors.append(label + ': 必须为数组')
            return []
        return value

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    def file_exists(value, label, sha=None):
        if not text(value):
            errors.append(label + ': 缺少文件路径')
            return None
        path = root / value
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(label + ': 文件不存在或为空')
            return None
        if sha is not None:
            valid_hash = (isinstance(sha, str) and len(sha) == 64
                          and all(c in '0123456789abcdef' for c in sha))
            need(valid_hash, label + ': 缺少有效SHA256')
            if valid_hash:
                need(hashlib.sha256(path.read_bytes()).hexdigest() == sha,
                     label + ': SHA256不一致')
        return path

    def evidence(values, label):
        values = arr(values, label)
        need(bool(values), label + ': 缺少证据')
        for value in values:
            file_exists(value, label)

    if not isinstance(record, dict):
        return ['记录必须为JSON对象']
    need(record.get('schema_version') == 2, '记录格式须为schema_version:2；旧记录保留，另建V2记录')
    mode = record.get('poster_mode')
    display = record.get('outline_display_mode')
    outline = record.get('has_outline')
    need(mode in ('single', 'split'), 'poster_mode须为single或split')
    need(type(outline) is bool, 'has_outline必须明确有无可用大纲')
    need(display in ('full', 'overview', 'none'), 'outline_display_mode须为full/overview/none')
    if display in ('full', 'overview'):
        need(outline is True, '展示完整大纲或方向概览需有真实大纲依据')
    if outline is False:
        need(display == 'none', '无可用大纲时不能虚构大纲或方向概览')
    if mode == 'split':
        need(outline is True and display == 'full', '双图须有真实大纲并选择full展示')
    need(record.get('facts_confirmed') is True, '本次使用的关键事实未确认')
    need(type(record.get('edit_mode')) is bool, 'edit_mode必须为布尔值')

    sources = arr(record.get('source_files'), 'source_files')
    need(bool(sources), '缺少真实资料来源')
    for value in sources:
        source = obj(value, '来源')
        file_exists(source.get('path'), '来源', source.get('sha256', ''))

    items = [obj(i, '文案条目') for i in arr(record.get('items'), 'items')]
    ids = [i.get('id') for i in items]
    need(bool(items), '文案清单为空')
    valid_ids = all(text(i) for i in ids)
    need(valid_ids and len(set(i for i in ids if isinstance(i, str))) == len(ids),
         '文案ID缺失、非字符串或重复')
    item_map = {i['id']: i for i in items if text(i.get('id'))}
    for item in items:
        label = str(item.get('id', '?'))
        need(text(item.get('text')) and text(item.get('source')), label + ': 原文或来源缺失')
        need(type(item.get('only_once')) is bool, label + ': only_once须为布尔值')
        page, kind = item.get('page'), item.get('kind')
        need(text(kind), label + ': 缺少kind')
        need(type(page) is int and page in ((1, 2) if mode == 'split' else (1,)), label + ': 页码错误')
        if kind == 'outline':
            need(display == 'full', label + ': 仅full可含完整大纲条目；overview用direction')
        if mode == 'split':
            if kind == 'outline':
                need(page == 2, label + ': 双图完整大纲必须在第2张')
            elif kind not in ('title', 'navigation'):
                need(page == 1, label + ': 非大纲信息必须在第1张')
    if display == 'full':
        need(any(i.get('kind') == 'outline' for i in items), 'full但清单没有大纲小点')
    if display == 'overview':
        need(any(i.get('kind') == 'direction' for i in items), 'overview须列真实方向概览条目kind:direction')

    design = obj(record.get('design_plan'), 'design_plan')
    file_exists(design.get('file'), '设计方案')
    need(design.get('confirmed') is True, '设计方向未确认或未沿用既有授权')
    route = obj(record.get('render_route'), 'render_route')
    route_kind = route.get('kind')
    need(route_kind in ('native', 'native_composite', 'html', 'hybrid'), '制作路线无效')
    file_exists(route.get('evidence'), '路线依据')
    if route_kind != 'native':
        need(route.get('authorized') is True, '替代或组合路线缺少客户授权记录')
    tool = obj(record.get('tool'), 'tool')
    need(text(tool.get('entry')) and text(tool.get('verified_at')), '工具入口或核验日期缺失')
    if route_kind in ('native', 'native_composite', 'hybrid'):
        need(tool.get('native') is True, '包含原生内容的路线需记录原生能力及真实溯源')
    file_exists(tool.get('evidence'), '工具能力证据')
    canvas = obj(record.get('canvas'), 'canvas')
    need(text(canvas.get('requested_ratio')) and text(canvas.get('rationale')), '画布方案或理由缺失')
    need(type(canvas.get('same_size')) is bool, 'canvas.same_size须明确')

    asset_role_names = ('reference', 'portrait', 'evidence', 'logo')
    requested = set()
    for role in arr(record.get('requested_roles', []), 'requested_roles'):
        need(isinstance(role, str) and role in asset_role_names, 'requested_roles: 角色无效')
        if isinstance(role, str) and role in asset_role_names:
            requested.add(role)
    assets = [obj(a, '素材角色') for a in arr(record.get('asset_roles'), 'asset_roles')]
    roles = set()
    for asset in assets:
        role = asset.get('role')
        need(role in asset_role_names, '素材role无效')
        if isinstance(role, str) and role in asset_role_names:
            roles.add(role)
        file_exists(asset.get('path'), '素材', asset.get('sha256', ''))
    if stage == 'final':
        for role in sorted(requested - roles):
            need(False, role + ': 客户已请求但尚无实际素材；不得抹去需求或宣告完成')
    edit = record.get('edit_mode') is True
    if edit:
        baseline = obj(record.get('baseline'), 'baseline')
        file_exists(baseline.get('file'), '修改基线', baseline.get('sha256', ''))
    reviews = obj(record.get('conditional_reviews'), 'conditional_reviews')
    for name in ('reference', 'portrait', 'evidence', 'revision'):
        review = obj(reviews.get(name), name + '分支验收')
        triggered = edit if name == 'revision' else name in roles or name in requested
        if triggered:
            missing_requested_asset = name in requested and name not in roles
            # A requested-but-missing asset is a pending need, never N/A.
            # An uploaded reference still requires completed design analysis.
            if stage == 'plan' and missing_requested_asset:
                need(review.get('status') in ('pending', 'running', 'waiting_for_key_material'),
                     name + ': 已请求但缺素材，须待补资料，不能记通过或不适用')
            elif stage == 'final' or name == 'reference':
                need(review.get('status') == 'passed', name + ': 已触发分支尚未通过')
                evidence(review.get('evidence'), name + '验收证据')
            else:
                need(review.get('status') in ('pending', 'running', 'waiting_for_key_material', 'passed'), name + ': 已触发分支不可记不适用')
                if review.get('status') == 'passed':
                    evidence(review.get('evidence'), name + '验收证据')
        else:
            need(review.get('status') == 'not_applicable' and text(review.get('reason')),
                 name + ': 未触发分支须不适用并说明理由')

    nodes = obj(record.get('nodes'), 'nodes')
    for index in range(1, 7 if stage == 'plan' else 13):
        key = 'P%02d' % index
        node = obj(nodes.get(key), key)
        if key == 'P10' and mode == 'single':
            need(node.get('status') == 'not_applicable' and text(node.get('reason')),
                 '单图P10须标不适用及理由')
        else:
            need(node.get('status') == 'passed', key + ': 核心节点尚未通过')
            evidence(node.get('evidence'), key + '证据')
    if stage == 'plan':
        return errors

    need(not record.get('open_issues'), '仍有未解决问题')
    pages = [obj(p, '页面') for p in arr(record.get('pages'), 'pages')]
    expected = 2 if mode == 'split' else 1
    need(len(pages) == expected, '最终图片数量错误')
    numbers = [p.get('page') for p in pages]
    need(all(type(n) is int for n in numbers) and sorted(numbers) == list(range(1, expected + 1)),
         '最终图片页码缺失或重复')
    observed, sizes = collections.Counter(), []
    for page in pages:
        number, label = page.get('page'), '第%s张' % page.get('page')
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
        production = page.get('production_mode')
        allowed = {'native': ('generated', 'native_reuse'),
                   'native_composite': ('generated', 'native_reuse'),
                   'html': ('html_render',),
                   'hybrid': ('generated', 'native_reuse', 'html_render')}
        need(production in allowed.get(route_kind, ()), label + ': 制作方式与路线不一致')
        if production == 'native_reuse' or route_kind == 'hybrid':
            file_exists(page.get('source_native_evidence'), label + '原生素材溯源')
        if route_kind in ('html', 'hybrid'):
            file_exists(page.get('editable_source'), label + '可编辑源文件')
        need(page.get('visual_review') == 'passed', label + ': 目视未通过')
        for item_id in arr(page.get('observed_items'), label + 'observed_items'):
            if not isinstance(item_id, str):
                errors.append(label + ': 观察文案ID必须为字符串')
                continue
            observed[item_id] += 1
            match = item_map.get(item_id)
            need(match is not None, label + ': 出现未知文案ID')
            if match:
                need(match.get('page') == number, label + ': 观察文案分配错误')
    if expected == 2 and canvas.get('same_size'):
        need(len(sizes) == 2 and sizes[0] == sizes[1], '双图实际尺寸不一致')
    for item in items:
        count = observed[item.get('id')] if text(item.get('id')) else 0
        need(count >= 1, str(item.get('id')) + ': 未在成图核实')
        if item.get('only_once') is True:
            need(count == 1, str(item.get('id')) + ': 只出现一次的文案重复')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--stage', choices=('plan', 'final'), default='final')
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding='utf-8'))
        errors = validate(record, args.record.resolve().parent, args.stage)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, struct.error) as exc:
        errors = ['无法读取有效记录: ' + str(exc)]
    print(json.dumps({'passed': not errors, 'stage': args.stage, 'errors': errors,
                      'scope': '仅验证结构、分支证据、哈希和像素头；不证明调用真实、文字准确、隐私完善或视觉质量'},
                     ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
