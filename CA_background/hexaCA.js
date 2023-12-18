// START HERE: https://www.redblobgames.com/grids/hexagons/
const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
console.log(ctx);
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

function draw() {}

let grid = [];
//console.log(grid);

function initGrid(mouse_pos, sq_dimension = 25) {
  let grid_width = Math.floor(canvas.width / sq_dimension);
  let grid_height = Math.floor(canvas.height / sq_dimension);
  let mouse_grid_x = Math.floor(mouse_pos[0] / sq_dimension);
  let mouse_grid_y = Math.floor(mouse_pos[1] / sq_dimension);
  //console.log(mouse_grid_x, mouse_grid_y);
  //console.log(grid_width, grid_height);
  grid = [];

  ctx.strokeStyle = "red";
  ctx.fillStyle = "red";
  ctx.strokeWidth = 2;
  for (let i of Array(grid_height).keys()) {
    let row = [];
    for (let j of Array(grid_width).keys()) {
      let cell = "";
      if (mouse_grid_x === j && mouse_grid_y === i) {
        ctx.fillRect(
          j * sq_dimension,
          i * sq_dimension,
          sq_dimension,
          sq_dimension
        );
        cell = "origin";
      } else {
        ctx.strokeRect(
          j * sq_dimension,
          i * sq_dimension,
          sq_dimension,
          sq_dimension
        );
      }
      row.push(cell);
    }
    grid.push(row);
  }
}
function getCursorPosition(canvas, event) {
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.left;
  //console.log(x, y);
  return [x, y];
}

let timer = null;
let animationInterval = null;

canvas.addEventListener("mousemove", function (event) {
  if (animationInterval) {
    clearInterval(animationInterval);
  }
  if (timer) {
    clearTimeout(timer);
  }
  const cursorPosition = getCursorPosition(canvas, event);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // Convert cursor position to hexagonal grid position and set the cell to "alive"
  //console.log(cursorPosition);

  initGrid(cursorPosition);
  /* after mousemove has cleaned/updated the background, kick off CA algo  */
  //console.log(grid);
  timer = setTimeout(() => {
    triggerAnimation(cursorPosition);
  }, 1000);
  //drawHexagon();
});
window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  initGrid([0, 0]);
});

canvas.addEventListener("mouseout", () => {
  console.log("leaving canvas: ", animationInterval);
  if (animationInterval) {
    clearInterval(animationInterval);
    animationInterval = null;
  }
});
canvas.addEventListener("mouseenter", () => {
  console.log("entering canvas at: ", animationInterval);
  if (animationInterval) {
    clearInterval(animationInterval);
    animationInterval = null;
  }
});

function getSquareNeighbors(x, y) {
  // Based on x and y, return the neighbors for a hexagon cell
  let neighbors = new Array(8).fill(null);
  let deltas = [
    [-1, -1],
    [-1, 0],
    [-1, 1],
    [0, -1],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1],
  ];
  for (let n = 0; n < neighbors.length; n++) {
    let n_delta = deltas.at(n);
    let y_delta = n_delta.at(1);
    let x_delta = n_delta.at(0);
    if (
      y + y_delta >= 0 &&
      y + y_delta < grid.length &&
      x + x_delta >= 0 &&
      x + x_delta < grid.at(0).length
    ) {
      neighbors[n] = [x + x_delta, y + y_delta];
    }
  }
  return neighbors;
}

function updateGrid() {
  // Implement your cellular automata rules and update the hexagonal grid
  /* iterate thru `grid`
  if item is origin, add neighbors to 'to_a';
  if item is "a", check neighbors, add neighbors to 'to_a' if empty or to 'to_d' if "a", add item to 'to_d' 
  if item is "d", continue
  update grid w/ to_- vals (first a's, then d's)?
  color accordingly
  */
  let to_a = [];
  let to_d = [];
  for (let i of grid.keys()) {
    for (let j of grid.at(i).keys()) {
      if (grid.at(i).at(j) === "origin") {
        neighbors = getSquareNeighbors(j, i);
      }
    }
  }
}

function triggerAnimation(cursorPosition) {
  if (animationInterval) clearInterval(animationInterval);

  animationInterval = setInterval(() => {
    updateGrid();
  }, 1000);
}

initGrid([0, 0]);
//animate();
