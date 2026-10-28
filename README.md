# loopny.net

Loop's website. 1 page, Edition 02 brand, logo drawn inline (NetFree blocks logo image files).

- Edit `src/index.src.html`, then run `python build.py`. It writes `docs/`, which GitHub Pages publishes.
- Contact form address: `form-endpoint.txt`. To send the form somewhere else, put the new address there and build again.
- Form script (Apps Script, owned by sterneizer@gmail.com): `form-script/`. It emails each message to loopworkflow@gmail.com. Change `SEND_TO` in `Code.js` to send elsewhere.
  - Editor: https://script.google.com/d/1CD_KIa_NNnTw-Ih0emNniP0tJn7byNSH5OoMSpX5KPwgZw1IZXA4jhBo/edit
  - Push: `clasp -P form-script/.clasp.json push -f`, then `clasp -P form-script/.clasp.json create-deployment -i [deployment id]` to update the live address in place. Run clasp with `-P`: a `.clasp.json` in the home folder catches it otherwise.
- Preview: the "loopny site (port 8766)" entry in `clients/We Trash/.claude/launch.json`.
