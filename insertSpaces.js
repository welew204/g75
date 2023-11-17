/* From Nathan interview... */
const sent = "hiplanetearth";
const dict = new Set(["hi", "planet", "plan", "earth"]);

function withSpaces(str, lookup) {
  let out = [];
  let test_string = "";
  let e = str.length;
  for (let i = str.length; i > -1; i--) {
    test_string = str.slice(i, e);
    if (lookup.has(test_string)) {
      out.unshift(test_string);
      e = i;
    }
  }
  return out;
}

console.log(withSpaces(sent, dict));
