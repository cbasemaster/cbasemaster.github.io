# cbasemaster.github.io

Personal GitHub Pages website for Novanto Yudistira.

## Local Preview

Open `index.html` directly in a browser, or run:

```powershell
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

## Deploy as a github.io Website

To publish this as:

```text
https://cbasemaster.github.io/
```

1. Create a GitHub repository named exactly `cbasemaster.github.io`.
2. Put `index.html`, `styles.css`, `script.js`, `.nojekyll`, and this `README.md` in the repository root.
3. Commit and push to the `main` branch.
4. Open repository Settings > Pages.
5. Under "Build and deployment", select "Deploy from a branch".
6. Select branch `main` and folder `/root`, then save.

GitHub usually publishes the website within a few minutes.
