# CONTRIBUTING.md

Thank you for your interest in contributing to roAp-Analysis!

## Contribution Guidelines

### Types of Contributions We Accept

1. **Bug Fixes** - Report and fix issues with analysis codes
2. **New Features** - Propose new asteroseismic analysis methods
3. **Documentation** - Improve docs, examples, and tutorials
4. **Tests** - Add or improve unit tests
5. **Performance** - Optimize code efficiency
6. **Scientific Methods** - Implement peer-reviewed techniques

### Getting Started

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/<yourusername>/roap-analysis.git`
3. **Create a branch**: `git checkout -b feature/my-feature`
4. **Make changes** and test thoroughly
5. **Commit**: `git commit -am 'Add my feature'`
6. **Push**: `git push origin feature/my-feature`
7. **Open a Pull Request**

### Code Standards

- **Python Style**: Follow PEP 8 (use `black` and `flake8`)
- **Documentation**: Add docstrings to all functions
- **Type Hints**: Use Python type annotations for clarity
- **Tests**: Include unit tests for new functionality

### Testing

Before submitting, ensure all tests pass:

```bash
pytest tests/
black src/roap_analysis
flake8 src/roap_analysis
```

### Scientific Rigor

When proposing new methods:
1. Reference published papers (DOI/arXiv)
2. Explain the physical/mathematical basis
3. Include validation against known results
4. Document uncertainties and limitations

### Questions?

Open an [Issue](https://github.com/yourusername/roap-analysis/issues) to discuss before large changes!

Thank you for contributing to roAp asteroseismology research! 🌟
