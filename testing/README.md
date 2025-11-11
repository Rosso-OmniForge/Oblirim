# OBLIRIM Testing Scripts

This folder contains all testing and verification scripts for the OBLIRIM project.

## Quick Start

From the main project directory, you can use the symlinked scripts:

```bash
# Quick start guide
./START_HERE.sh

# Simple TUI test
./test-tui-simple.sh

# Verify TUI fixes
./verify-tui-fixes.sh
```

Or run directly from the testing folder:

```bash
cd testing/

# All available scripts
./START_HERE.sh              # Quick start guide
./verify-tui-fixes.sh        # Verify TUI fixes
./test-tui-checklist.sh      # Comprehensive TUI checklist
./test-tui-simple.sh         # Simple TUI test
./test-tui.sh                # Full TUI test with backend
./test_tui_standalone.py     # Standalone Python TUI test
./test-dev.sh                # Development testing
./test-installation.sh       # Installation verification
./test-service.sh            # Service testing
```

---

## Script Descriptions

### TUI Testing

**START_HERE.sh**
- Quick start guide for testing the fixed TUI
- Shows overview and runs verification
- Best for first-time testing

**verify-tui-fixes.sh**
- Quick verification of TUI fixes
- Checks syntax, dependencies, imports
- Fast automated checks

**test-tui-checklist.sh**
- Comprehensive testing checklist
- Automated + manual verification
- Shows all 8 test points

**test-tui-simple.sh**
- Simple TUI test with auto-setup
- Creates venv if needed
- Easiest way to test TUI

**test-tui.sh**
- Full TUI test with backend check
- Starts backend server if needed
- Most comprehensive TUI test

**test_tui_standalone.py**
- Python standalone test
- No backend required
- Good for isolated testing

### System Testing

**test-dev.sh**
- Development environment testing
- Quick checks during development

**test-installation.sh**
- Verifies installation completed correctly
- Checks all dependencies

**test-service.sh**
- Tests systemd service
- Verifies service configuration

---

## Symlinks

The following symlinks exist in the main directory for convenience:

- `START_HERE.sh` → `testing/START_HERE.sh`
- `test-tui-simple.sh` → `testing/test-tui-simple.sh`
- `verify-tui-fixes.sh` → `testing/verify-tui-fixes.sh`

These allow you to run the most common tests from the main directory without changing into the testing folder.

---

## Adding New Tests

When adding new test scripts:

1. Place them in this `testing/` folder
2. Make them executable: `chmod +x script.sh`
3. If commonly used, create a symlink in the main directory:
   ```bash
   ln -s testing/your-script.sh your-script.sh
   ```

---

## Organization Benefits

✅ **Clean Main Directory** - Only essential files in root  
✅ **Organized Tests** - All testing scripts in one place  
✅ **Easy Access** - Symlinks for frequently used scripts  
✅ **Scalable** - Easy to add more tests  

---

## Documentation

Related documentation:
- `/docs/TUI_FIXES.md` - TUI fix documentation
- `/docs/TESTING_GUIDE.md` - General testing guide
- `/TUI_FIX_SUMMARY.md` - TUI fix summary
- `/TUI_COMPLETE.md` - Complete TUI review

---

**All test scripts are organized here for easy maintenance and a clean project structure!**
