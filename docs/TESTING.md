# Testing Scripts Organization

All test and verification scripts have been moved to the `testing/` folder to keep the main project directory clean.

## Quick Access (Symlinked Scripts)

The most frequently used scripts are symlinked in the main directory:

```bash
./START_HERE.sh          # → testing/START_HERE.sh
./test-tui-simple.sh     # → testing/test-tui-simple.sh
./verify-tui-fixes.sh    # → testing/verify-tui-fixes.sh
```

## All Testing Scripts

To see all available test scripts:

```bash
ls testing/
```

Or read the testing documentation:

```bash
cat testing/README.md
```

## Available Tests

### Quick Start
```bash
./START_HERE.sh              # Interactive quick start guide
```

### TUI Testing
```bash
./verify-tui-fixes.sh        # Quick verification (recommended first)
./test-tui-simple.sh         # Simple TUI test
testing/test-tui.sh          # Full TUI test with backend
testing/test-tui-checklist.sh # Comprehensive checklist
testing/test_tui_standalone.py # Standalone Python test
```

### System Testing
```bash
testing/test-dev.sh          # Development testing
testing/test-installation.sh # Installation verification
testing/test-service.sh      # Service testing
testing/quick-test.sh        # Quick system test
```

## Why This Organization?

✅ **Clean main directory** - Only essential project files in root  
✅ **Easy to find** - All tests in one place  
✅ **Convenient access** - Symlinks for common scripts  
✅ **Scalable** - Easy to add new tests  

## More Information

- **testing/README.md** - Complete testing documentation
- **docs/TESTING_GUIDE.md** - General testing guide
- **TUI_FIX_SUMMARY.md** - TUI fixes overview
