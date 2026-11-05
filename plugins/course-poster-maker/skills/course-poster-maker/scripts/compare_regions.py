#!/usr/bin/env python3
"""Read-only decoded-pixel comparison. Never sharpens, redraws or edits images."""
import argparse
import hashlib
import json
from pathlib import Path


def parse_rectangle(value):
    try:
        rect = [int(i) for i in value.split(',')]
    except ValueError as exc:
        raise argparse.ArgumentTypeError('区域须为整数x,y,width,height') from exc
    if len(rect) != 4 or min(rect[:2]) < 0 or min(rect[2:]) <= 0:
        raise argparse.ArgumentTypeError('区域须为非负x/y和正width/height')
    return rect


def compare(baseline, candidate, allowed):
    try:
        from PIL import Image, ImageChops, ImageDraw
    except ImportError as exc:
        raise RuntimeError('像素比较需要Pillow；请使用平台已有Pillow运行环境，或经客户允许安装。没有此依赖仍可人工逐区对照，不能伪报0变化。') from exc
    with Image.open(baseline) as before, Image.open(candidate) as after:
        before.load()
        after.load()
        if before.size != after.size:
            raise ValueError('图片尺寸不同，不能进行同坐标冻结区核验；先记录获授权的几何变化并采用对应检查')
        if any(x + w > before.width or y + h > before.height for x, y, w, h in allowed):
            raise ValueError('允许变化区域超出图片边界')
        original_modes = [before.mode, after.mode]
        if before.mode not in ('RGB', 'RGBA', 'L', 'LA', 'P') or after.mode not in ('RGB', 'RGBA', 'L', 'LA', 'P'):
            raise ValueError('仅比较8位常规图像；16位/HDR/特殊色彩模式需专门核验，不能转码后声称原像素不变')
        diff = ImageChops.difference(before.convert('RGBA'), after.convert('RGBA'))
        bands = diff.split()
        mask = bands[0]
        for band in bands[1:]:
            mask = ImageChops.lighter(mask, band)
        mask = mask.point(lambda v: 255 if v else 0)
        changed = mask.histogram()[255]
        allow = Image.new('L', before.size, 0)
        draw = ImageDraw.Draw(allow)
        for x, y, w, h in allowed:
            draw.rectangle((x, y, x + w - 1, y + h - 1), fill=255)
        outside = ImageChops.subtract(mask, allow).histogram()[255]
        return {
            'baseline': str(baseline), 'candidate': str(candidate),
            'baseline_sha256': hashlib.sha256(baseline.read_bytes()).hexdigest(),
            'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
            'size': list(before.size), 'original_modes': original_modes,
            'comparison': 'decoded 8-bit RGBA pixels; no resampling; metadata and profiles not assessed',
            'allowed_regions': allowed, 'changed_pixels': changed,
            'changed_outside_allowed_regions': outside, 'passed': outside == 0,
            'scope': '仅证明冻结区域解码像素一致；不证明文字可读、来源真实、隐私完整或审美通过'
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path)
    parser.add_argument('candidate', type=Path)
    parser.add_argument('--allowed', action='append', type=parse_rectangle, default=[], metavar='X,Y,W,H')
    parser.add_argument('--output', type=Path, help='可选的新JSON报告，不覆盖已有文件或输入图片')
    args = parser.parse_args()
    try:
        if args.output and (args.output.exists() or args.output.resolve() in (args.baseline.resolve(), args.candidate.resolve())):
            raise ValueError('报告路径已存在或与输入相同；请指定新的JSON报告路径')
        report = compare(args.baseline, args.candidate, args.allowed)
        output = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
        if args.output:
            args.output.write_text(output, encoding='utf-8')
        print(output, end='')
        return 0 if report['passed'] else 1
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({'passed': False, 'error': str(exc)}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
