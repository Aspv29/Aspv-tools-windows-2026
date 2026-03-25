#!/bin/bash
# ASPV Tools - Build Verification Script
# Verifies that all files are present and the build is complete

echo "=========================================="
echo "ASPV Tools v2.0 - Build Verification"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $1 - MISSING"
        ((FAILED++))
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $1/ - MISSING"
        ((FAILED++))
    fi
}

echo "Checking Core Files..."
echo "----------------------"
check_file "aspv_tools.py"
check_file "ASPVTools.spec"
check_file "requirements.txt"
echo ""

echo "Checking Build Scripts..."
echo "-------------------------"
check_file "build_exe.bat"
check_file "build_exe.ps1"
check_file "build_exe.sh"
echo ""

echo "Checking Documentation..."
echo "-------------------------"
check_file "README.md"
check_file "INSTALL.md"
check_file "CHANGELOG.md"
check_file "CONTRIBUTING.md"
check_file "LICENSE"
check_file "PROJECT_SUMMARY.md"
echo ""

echo "Checking Configuration..."
echo "-------------------------"
check_file ".gitignore"
check_dir ".blackbox"
echo ""

echo "Checking Build Output..."
echo "------------------------"
check_dir "dist"
check_file "dist/ASPVTools"
echo ""

# Check executable permissions
if [ -f "dist/ASPVTools" ]; then
    if [ -x "dist/ASPVTools" ]; then
        echo -e "${GREEN}✓${NC} Executable has correct permissions"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} Executable missing execute permission"
        echo "  Run: chmod +x dist/ASPVTools"
    fi
fi

# Check build script permissions
if [ -f "build_exe.sh" ]; then
    if [ -x "build_exe.sh" ]; then
        echo -e "${GREEN}✓${NC} Build script has execute permission"
        ((PASSED++))
    else
        echo -e "${YELLOW}⚠${NC} Build script missing execute permission"
        echo "  Run: chmod +x build_exe.sh"
    fi
fi

echo ""
echo "File Sizes..."
echo "-------------"
if [ -f "aspv_tools.py" ]; then
    SIZE=$(du -h aspv_tools.py | cut -f1)
    echo "aspv_tools.py: $SIZE"
fi

if [ -f "dist/ASPVTools" ]; then
    SIZE=$(du -h dist/ASPVTools | cut -f1)
    echo "dist/ASPVTools: $SIZE"
fi

echo ""
echo "Python Syntax Check..."
echo "----------------------"
if command -v python3 &> /dev/null; then
    if python3 -m py_compile aspv_tools.py 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Python syntax is valid"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} Python syntax errors found"
        ((FAILED++))
    fi
else
    echo -e "${YELLOW}⚠${NC} Python3 not found, skipping syntax check"
fi

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ BUILD VERIFICATION SUCCESSFUL${NC}"
    echo ""
    echo "All files are present and the build is complete!"
    echo ""
    echo "Next steps:"
    echo "  1. Test the executable: ./dist/ASPVTools"
    echo "  2. Read documentation: cat README.md"
    echo "  3. Check installation guide: cat INSTALL.md"
    echo ""
    exit 0
else
    echo -e "${RED}❌ BUILD VERIFICATION FAILED${NC}"
    echo ""
    echo "Some files are missing. Please rebuild the project."
    echo ""
    exit 1
fi
