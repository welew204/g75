// START HERE: https://www.redblobgames.com/grids/hexagons/
const canvas = document.getElementById("myCanvas");
const ctx = canvas.getContext("2d");
console.log(ctx);
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

function draw() {}

let grid = [];
console.log(grid);

function initGrid(mouse_pos, sq_dimension = 30) {
  let grid_width = Math.floor(canvas.width / sq_dimension);
  let grid_height = Math.floor(canvas.height / sq_dimension);
  let mouse_grid_x = Math.floor(mouse_pos[0] / sq_dimension);
  let mouse_grid_y = Math.floor(mouse_pos[1] / sq_dimension);
  //console.log(mouse_grid_x, mouse_grid_y);

  ctx.strokeStyle = "red";
  ctx.fillStyle = "red";
  ctx.strokeWidth = 2;
  for (let i of Array(grid_height).keys()) {
    for (let j of Array(grid_width).keys()) {
      if (mouse_grid_x === j && mouse_grid_y === i) {
        ctx.fillRect(
          j * sq_dimension,
          i * sq_dimension,
          sq_dimension,
          sq_dimension
        );
      } else {
        ctx.strokeRect(
          j * sq_dimension,
          i * sq_dimension,
          sq_dimension,
          sq_dimension
        );
      }
    }
  }
}
function getCursorPosition(canvas, event) {
  const rect = canvas.getBoundingClientRect();
  const x = event.clientX - rect.left;
  const y = event.clientY - rect.left;
  //console.log(x, y);
  return [x, y];
}
canvas.addEventListener("mousemove", function (event) {
  const cursorPosition = getCursorPosition(canvas, event);
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // Convert cursor position to hexagonal grid position and set the cell to "alive"
  //console.log(cursorPosition);
  [x, y] = cursorPosition;
  initGrid(cursorPosition);
  //drawHexagon();
});
window.addEventListener("resize", () => {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  initGrid([0, 0]);
});
function getHexagonNeighbors(x, y) {
  // Based on x and y, return the neighbors for a hexagon cell
}

function updateGrid() {
  // Implement your cellular automata rules and update the hexagonal grid
}

function drawHexagon(x, y) {
  // Use the canvas 2D API to draw a polygon at (x, y) with the specified size
}

function render() {
  // Draw the hexagonal grid on the canvas based on cell states
}

function animate() {
  requestAnimationFrame(animate);
  updateGrid();
  render();
}

initGrid([0, 0]);
//animate();
