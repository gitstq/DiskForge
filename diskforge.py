#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DiskForge - Lightweight Terminal Disk Usage Analyzer Engine
轻量级终端磁盘使用分析引擎

A zero-dependency disk usage analyzer with TUI dashboard,
duplicate detection, and multi-format reporting.

Author: DiskForge Team
License: MIT
Version: 1.0.0
"""

import os
import sys
import hashlib
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
import threading
import time

# Try to import curses for TUI, fallback to basic mode if not available
try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False


@dataclass
class FileInfo:
    """File information container"""
    path: str
    size: int
    is_dir: bool
    mtime: float
    extension: str = ""
    
    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "size": self.size,
            "is_dir": self.is_dir,
            "mtime": self.mtime,
            "extension": self.extension
        }


@dataclass
class ScanResult:
    """Scan result container"""
    root_path: str
    total_size: int = 0
    total_files: int = 0
    total_dirs: int = 0
    files: List[FileInfo] = field(default_factory=list)
    by_extension: Dict[str, int] = field(default_factory=dict)
    by_extension_count: Dict[str, int] = field(default_factory=dict)
    large_files: List[FileInfo] = field(default_factory=list)
    duplicates: List[List[FileInfo]] = field(default_factory=list)
    scan_time: float = 0.0
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            "root_path": self.root_path,
            "total_size": self.total_size,
            "total_files": self.total_files,
            "total_dirs": self.total_dirs,
            "scan_time": self.scan_time,
            "by_extension": self.by_extension,
            "by_extension_count": self.by_extension_count,
            "large_files": [f.to_dict() for f in self.large_files],
            "duplicates": [[f.to_dict() for f in group] for group in self.duplicates],
            "errors": self.errors
        }


class DiskScanner:
    """Core disk scanning engine"""
    
    def __init__(self, 
                 path: str, 
                 min_size: int = 0,
                 max_depth: int = -1,
                 exclude_dirs: Set[str] = None,
                 progress_callback=None):
        self.path = Path(path).resolve()
        self.min_size = min_size
        self.max_depth = max_depth
        self.exclude_dirs = exclude_dirs or {'.git', '__pycache__', 'node_modules', '.venv', 'venv'}
        self.progress_callback = progress_callback
        self._stop_flag = False
        
    def stop(self):
        """Stop the scan"""
        self._stop_flag = True
        
    def scan(self) -> ScanResult:
        """Perform the disk scan"""
        start_time = time.time()
        result = ScanResult(root_path=str(self.path))
        
        if not self.path.exists():
            result.errors.append(f"Path does not exist: {self.path}")
            return result
            
        self._scan_dir(self.path, result, depth=0)
        
        # Sort files by size
        result.files.sort(key=lambda x: x.size, reverse=True)
        
        # Get top large files
        result.large_files = result.files[:50]
        
        # Calculate scan time
        result.scan_time = time.time() - start_time
        
        return result
    
    def _scan_dir(self, path: Path, result: ScanResult, depth: int):
        """Recursively scan directory"""
        if self._stop_flag:
            return
            
        if self.max_depth >= 0 and depth > self.max_depth:
            return
            
        try:
            for entry in path.iterdir():
                if self._stop_flag:
                    return
                    
                try:
                    # Skip excluded directories
                    if entry.is_dir() and entry.name in self.exclude_dirs:
                        continue
                        
                    if entry.is_file():
                        stat = entry.stat()
                        size = stat.st_size
                        
                        if size >= self.min_size:
                            ext = entry.suffix.lower() or "(no extension)"
                            file_info = FileInfo(
                                path=str(entry),
                                size=size,
                                is_dir=False,
                                mtime=stat.st_mtime,
                                extension=ext
                            )
                            result.files.append(file_info)
                            result.total_size += size
                            result.total_files += 1
                            
                            # Extension statistics
                            result.by_extension[ext] = result.by_extension.get(ext, 0) + size
                            result.by_extension_count[ext] = result.by_extension_count.get(ext, 0) + 1
                            
                            if self.progress_callback:
                                self.progress_callback(result.total_files, result.total_size, str(entry))
                                
                    elif entry.is_dir():
                        result.total_dirs += 1
                        self._scan_dir(entry, result, depth + 1)
                        
                except (PermissionError, OSError) as e:
                    result.errors.append(f"Access denied: {entry}: {e}")
                    
        except (PermissionError, OSError) as e:
            result.errors.append(f"Cannot read directory {path}: {e}")


class DuplicateDetector:
    """Detect duplicate files based on size and hash"""
    
    def __init__(self, files: List[FileInfo], progress_callback=None):
        self.files = files
        self.progress_callback = progress_callback
        
    def detect(self) -> List[List[FileInfo]]:
        """Find duplicate files"""
        # Group by size first
        by_size: Dict[int, List[FileInfo]] = defaultdict(list)
        for f in self.files:
            by_size[f.size].append(f)
            
        # Only check files with same size
        potential_dups = {k: v for k, v in by_size.items() if len(v) > 1}
        
        duplicates = []
        checked = 0
        total = sum(len(v) for v in potential_dups.values())
        
        for size, file_list in potential_dups.items():
            # Group by hash
            by_hash: Dict[str, List[FileInfo]] = defaultdict(list)
            
            for f in file_list:
                try:
                    file_hash = self._calculate_hash(f.path)
                    by_hash[file_hash].append(f)
                except (IOError, OSError):
                    pass
                    
                checked += 1
                if self.progress_callback:
                    self.progress_callback(checked, total)
                    
            # Add groups with more than 1 file
            for group in by_hash.values():
                if len(group) > 1:
                    duplicates.append(group)
                    
        return duplicates
    
    def _calculate_hash(self, filepath: str, chunk_size: int = 8192) -> str:
        """Calculate MD5 hash of file"""
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(chunk_size), b''):
                    hasher.update(chunk)
        except (IOError, OSError):
            return ""
        return hasher.hexdigest()


class ReportGenerator:
    """Generate reports in multiple formats"""
    
    @staticmethod
    def format_size(size: int) -> str:
        """Format size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    
    @staticmethod
    def to_json(result: ScanResult, output_path: str = None) -> str:
        """Generate JSON report"""
        data = result.to_dict()
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
        return json_str
    
    @staticmethod
    def to_markdown(result: ScanResult, output_path: str = None) -> str:
        """Generate Markdown report"""
        lines = [
            f"# DiskForge Analysis Report",
            f"",
            f"**Scan Path:** `{result.root_path}`",
            f"**Scan Time:** {result.scan_time:.2f}s",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"## Summary",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Size | {ReportGenerator.format_size(result.total_size)} |",
            f"| Total Files | {result.total_files:,} |",
            f"| Total Directories | {result.total_dirs:,} |",
            f"",
            f"## Top 10 Largest Files",
            f"",
        ]
        
        for i, f in enumerate(result.large_files[:10], 1):
            lines.append(f"{i}. `{Path(f.path).name}` - {ReportGenerator.format_size(f.size)}")
            
        lines.extend([
            f"",
            f"## Space by File Type",
            f"",
            f"| Extension | Size | Count |",
            f"|-----------|------|-------|",
        ])
        
        sorted_ext = sorted(result.by_extension.items(), key=lambda x: x[1], reverse=True)[:15]
        for ext, size in sorted_ext:
            count = result.by_extension_count.get(ext, 0)
            lines.append(f"| {ext} | {ReportGenerator.format_size(size)} | {count:,} |")
            
        if result.duplicates:
            lines.extend([
                f"",
                f"## Duplicate Files ({len(result.duplicates)} groups)",
                f"",
            ])
            for i, group in enumerate(result.duplicates[:10], 1):
                wasted = sum(f.size for f in group[1:])
                lines.append(f"### Group {i} (Wasted: {ReportGenerator.format_size(wasted)})")
                for f in group:
                    lines.append(f"- `{f.path}`")
                lines.append("")
                
        content = "\n".join(lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return content
    
    @staticmethod
    def to_html(result: ScanResult, output_path: str = None) -> str:
        """Generate HTML report"""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DiskForge Report - {result.root_path}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .stat-card h3 {{ margin: 0; font-size: 2em; }}
        .stat-card p {{ margin: 5px 0 0; opacity: 0.9; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        tr:hover {{ background: #f5f5f5; }}
        .size-bar {{ background: #e0e0e0; border-radius: 5px; overflow: hidden; }}
        .size-bar-fill {{ background: linear-gradient(90deg, #4CAF50, #8BC34A); height: 20px; }}
        .footer {{ margin-top: 30px; text-align: center; color: #888; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>💾 DiskForge Analysis Report</h1>
        <p><strong>Path:</strong> <code>{result.root_path}</code></p>
        <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat-card">
                <h3>{ReportGenerator.format_size(result.total_size)}</h3>
                <p>Total Size</p>
            </div>
            <div class="stat-card">
                <h3>{result.total_files:,}</h3>
                <p>Total Files</p>
            </div>
            <div class="stat-card">
                <h3>{result.total_dirs:,}</h3>
                <p>Directories</p>
            </div>
            <div class="stat-card">
                <h3>{result.scan_time:.2f}s</h3>
                <p>Scan Time</p>
            </div>
        </div>
        
        <h2>📊 Top 20 Largest Files</h2>
        <table>
            <tr><th>#</th><th>File</th><th>Size</th><th>Modified</th></tr>
"""
        
        for i, f in enumerate(result.large_files[:20], 1):
            mtime = datetime.fromtimestamp(f.mtime).strftime('%Y-%m-%d %H:%M')
            name = Path(f.path).name
            html += f"            <tr><td>{i}</td><td title=\"{f.path}\">{name[:50]}{'...' if len(name) > 50 else ''}</td><td>{ReportGenerator.format_size(f.size)}</td><td>{mtime}</td></tr>\n"
            
        html += """        </table>
        
        <h2>📁 Space by File Type</h2>
        <table>
            <tr><th>Extension</th><th>Size</th><th>Count</th><th>Distribution</th></tr>
"""
        
        max_ext_size = max(result.by_extension.values()) if result.by_extension else 1
        sorted_ext = sorted(result.by_extension.items(), key=lambda x: x[1], reverse=True)[:20]
        
        for ext, size in sorted_ext:
            count = result.by_extension_count.get(ext, 0)
            pct = (size / max_ext_size) * 100
            html += f"""            <tr>
                <td><code>{ext}</code></td>
                <td>{ReportGenerator.format_size(size)}</td>
                <td>{count:,}</td>
                <td><div class="size-bar"><div class="size-bar-fill" style="width: {pct:.1f}%"></div></div></td>
            </tr>
"""
            
        html += f"""        </table>
        
        <div class="footer">
            <p>Generated by <strong>DiskForge</strong> - Lightweight Terminal Disk Usage Analyzer</p>
        </div>
    </div>
</body>
</html>"""
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
        return html


class TUIDashboard:
    """Terminal User Interface Dashboard"""
    
    def __init__(self, result: ScanResult):
        self.result = result
        self.selected = 0
        self.scroll_offset = 0
        self.view_mode = "files"  # files, extensions, duplicates
        
    def run(self):
        """Run the TUI dashboard"""
        if not CURSES_AVAILABLE:
            print("Curses not available. Falling back to text output.")
            self._print_text_summary()
            return
            
        try:
            curses.wrapper(self._main_loop)
        except KeyboardInterrupt:
            pass
            
    def _main_loop(self, stdscr):
        """Main TUI loop"""
        curses.curs_set(0)
        stdscr.nodelay(1)
        
        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            
            # Header
            header = f" 💾 DiskForge - {self.result.root_path} "
            stdscr.addstr(0, 0, header.center(w, "="), curses.A_REVERSE)
            
            # Stats bar
            stats = f" 📊 Total: {ReportGenerator.format_size(self.result.total_size)} | Files: {self.result.total_files:,} | Dirs: {self.result.total_dirs:,} | Time: {self.result.scan_time:.2f}s "
            stdscr.addstr(1, 0, stats[:w], curses.A_BOLD)
            
            # Tab bar
            tabs = ["[F] Files", "[E] Extensions", "[D] Duplicates", "[Q] Quit"]
            tab_str = "  ".join(tabs)
            stdscr.addstr(2, 0, tab_str[:w], curses.A_UNDERLINE)
            
            # Content area
            content_start = 4
            content_height = h - content_start - 1
            
            if self.view_mode == "files":
                self._draw_files(stdscr, content_start, content_height, w)
            elif self.view_mode == "extensions":
                self._draw_extensions(stdscr, content_start, content_height, w)
            elif self.view_mode == "duplicates":
                self._draw_duplicates(stdscr, content_start, content_height, w)
                
            # Footer
            stdscr.addstr(h - 1, 0, " ↑↓ Navigate | Enter: Details | Q: Quit ".center(w), curses.A_REVERSE)
            
            stdscr.refresh()
            
            # Handle input
            try:
                key = stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break
                elif key == ord('f') or key == ord('F'):
                    self.view_mode = "files"
                    self.selected = 0
                    self.scroll_offset = 0
                elif key == ord('e') or key == ord('E'):
                    self.view_mode = "extensions"
                    self.selected = 0
                    self.scroll_offset = 0
                elif key == ord('d') or key == ord('D'):
                    self.view_mode = "duplicates"
                    self.selected = 0
                    self.scroll_offset = 0
                elif key == curses.KEY_UP:
                    self.selected = max(0, self.selected - 1)
                elif key == curses.KEY_DOWN:
                    max_items = self._get_max_items()
                    self.selected = min(max_items - 1, self.selected + 1)
                elif key == curses.KEY_PPAGE:
                    self.selected = max(0, self.selected - 10)
                elif key == curses.KEY_NPAGE:
                    max_items = self._get_max_items()
                    self.selected = min(max_items - 1, self.selected + 10)
            except:
                pass
                
    def _get_max_items(self) -> int:
        if self.view_mode == "files":
            return len(self.result.large_files)
        elif self.view_mode == "extensions":
            return len(self.result.by_extension)
        elif self.view_mode == "duplicates":
            return len(self.result.duplicates)
        return 0
        
    def _draw_files(self, stdscr, start, height, width):
        """Draw files list"""
        files = self.result.large_files
        visible = files[self.scroll_offset:self.scroll_offset + height]
        
        for i, f in enumerate(visible):
            idx = self.scroll_offset + i
            attr = curses.A_REVERSE if idx == self.selected else 0
            size_str = ReportGenerator.format_size(f.size).rjust(12)
            name = Path(f.path).name[:width - 20]
            line = f" {size_str}  {name}"
            stdscr.addstr(start + i, 0, line[:width], attr)
            
    def _draw_extensions(self, stdscr, start, height, width):
        """Draw extensions list"""
        sorted_ext = sorted(self.result.by_extension.items(), key=lambda x: x[1], reverse=True)
        visible = sorted_ext[self.scroll_offset:self.scroll_offset + height]
        max_size = max(self.result.by_extension.values()) if self.result.by_extension else 1
        
        for i, (ext, size) in enumerate(visible):
            idx = self.scroll_offset + i
            attr = curses.A_REVERSE if idx == self.selected else 0
            count = self.result.by_extension_count.get(ext, 0)
            size_str = ReportGenerator.format_size(size).rjust(12)
            bar_width = int((size / max_size) * 20)
            bar = "█" * bar_width
            line = f" {ext:15} {size_str}  {count:6,}  {bar}"
            stdscr.addstr(start + i, 0, line[:width], attr)
            
    def _draw_duplicates(self, stdscr, start, height, width):
        """Draw duplicates list"""
        if not self.result.duplicates:
            stdscr.addstr(start, 0, " No duplicates found ".center(width))
            return
            
        visible = self.result.duplicates[self.scroll_offset:self.scroll_offset + height]
        
        for i, group in enumerate(visible):
            idx = self.scroll_offset + i
            attr = curses.A_REVERSE if idx == self.selected else 0
            wasted = sum(f.size for f in group[1:])
            size_str = ReportGenerator.format_size(wasted).rjust(12)
            line = f" {size_str} wasted  |  {len(group)} files  |  {Path(group[0].path).name[:30]}"
            stdscr.addstr(start + i, 0, line[:width], attr)
            
    def _print_text_summary(self):
        """Print text summary when curses not available"""
        print("\n" + "=" * 60)
        print(f"  DiskForge Analysis: {self.result.root_path}")
        print("=" * 60)
        print(f"\n  Total Size: {ReportGenerator.format_size(self.result.total_size)}")
        print(f"  Total Files: {self.result.total_files:,}")
        print(f"  Total Dirs: {self.result.total_dirs:,}")
        print(f"  Scan Time: {self.result.scan_time:.2f}s")
        
        print("\n  Top 10 Largest Files:")
        for i, f in enumerate(self.result.large_files[:10], 1):
            print(f"    {i}. {ReportGenerator.format_size(f.size):>12}  {Path(f.path).name}")
            
        print("\n  Top 10 File Types:")
        sorted_ext = sorted(self.result.by_extension.items(), key=lambda x: x[1], reverse=True)[:10]
        for ext, size in sorted_ext:
            count = self.result.by_extension_count.get(ext, 0)
            print(f"    {ext:15} {ReportGenerator.format_size(size):>12}  ({count:,} files)")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="DiskForge - Lightweight Terminal Disk Usage Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  diskforge /path/to/scan              Scan and show TUI dashboard
  diskforge /path --json report.json   Export JSON report
  diskforge /path --html report.html   Export HTML report
  diskforge /path --find-dups          Find duplicate files
  diskforge /path --min-size 100MB     Only files >= 100MB
        """
    )
    
    parser.add_argument("path", help="Path to scan")
    parser.add_argument("--json", metavar="FILE", help="Export JSON report")
    parser.add_argument("--markdown", "--md", metavar="FILE", help="Export Markdown report")
    parser.add_argument("--html", metavar="FILE", help="Export HTML report")
    parser.add_argument("--min-size", default="0", help="Minimum file size (e.g., 100MB, 1GB)")
    parser.add_argument("--max-depth", type=int, default=-1, help="Maximum scan depth")
    parser.add_argument("--find-dups", action="store_true", help="Find duplicate files")
    parser.add_argument("--no-tui", action="store_true", help="Disable TUI, print summary")
    parser.add_argument("--version", action="version", version="DiskForge 1.0.0")
    
    args = parser.parse_args()
    
    # Parse min size
    min_size = parse_size(args.min_size)
    
    print(f"🔍 Scanning {args.path}...")
    
    # Create scanner
    scanner = DiskScanner(
        path=args.path,
        min_size=min_size,
        max_depth=args.max_depth
    )
    
    # Run scan
    result = scanner.scan()
    
    print(f"✅ Scan complete: {result.total_files:,} files, {ReportGenerator.format_size(result.total_size)}")
    
    # Find duplicates if requested
    if args.find_dups:
        print("🔍 Finding duplicates...")
        detector = DuplicateDetector(result.files)
        result.duplicates = detector.detect()
        print(f"✅ Found {len(result.duplicates)} duplicate groups")
        
    # Export reports
    if args.json:
        ReportGenerator.to_json(result, args.json)
        print(f"📄 JSON report saved to {args.json}")
        
    if args.markdown:
        ReportGenerator.to_markdown(result, args.markdown)
        print(f"📄 Markdown report saved to {args.markdown}")
        
    if args.html:
        ReportGenerator.to_html(result, args.html)
        print(f"📄 HTML report saved to {args.html}")
        
    # Show TUI or text summary
    if not (args.json or args.markdown or args.html) or not args.no_tui:
        if args.no_tui or not CURSES_AVAILABLE:
            TUIDashboard(result)._print_text_summary()
        else:
            dashboard = TUIDashboard(result)
            dashboard.run()


def parse_size(size_str: str) -> int:
    """Parse size string like '100MB' to bytes"""
    size_str = size_str.upper().strip()
    
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
        'TB': 1024 ** 4,
    }
    
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            try:
                return int(float(size_str[:-len(unit)]) * multiplier)
            except ValueError:
                pass
                
    try:
        return int(size_str)
    except ValueError:
        return 0


if __name__ == "__main__":
    main()
