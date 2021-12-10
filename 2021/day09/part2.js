const fs = require('fs')

async function main() {
  const rawData = fs.readFileSync('./data-input', 'utf-8');
  const inputs = rawData.split('\n').map(d => {
    return d
  })

  const grid = parse(inputs);
  const result = solve(grid)

  console.log('result: ', result)
}

function parse(inputs) {
  const grid = [];
  for (let i = 0; i < inputs.length; i++) {
    const g = inputs[i].split('').map(d => parseInt(d, 10))
    grid.push(g)
  }

  return grid
}


const DELTA = [
  [-1, 0],
  [1, 0],
  [0, -1],
  [0, 1],
]
function basinSize(grid, x, y) {
  if (grid[x][y] === 9) {
    return 0
  }
  const seen = []
  grid.forEach(element => {
    seen.push(new Array(element.length).fill(false))
  });

  console.log(`basinSize: ${x} ${y} ***`)
  const q = [[x, y]]
  seen[x][y] = true

  let size = 0;
  while (q.length > 0) {
    const next = q.shift();
    // console.log('next', next)
    size++

    const curr = grid[next[0]][next[1]]
    console.log('x: ', next[0], ' y: ', next[1], '*curr*: ', curr)
    for (let i = 0; i < DELTA.length; i++) {
      const dx = next[0] + DELTA[i][0];
      const dy = next[1] + DELTA[i][1];

      if (dx < 0 || dx >= grid.length) {
        continue;
      }

      // console.log(dx, typeof dx, dy, typeof dy)
      if (dy < 0 || dy >= grid[dx].length) {
        continue;
      }

      if (grid[dx][dy] === 9 || seen[dx][dy]) {
        continue;
      }

      const surr = grid[dx][dy]
      console.log('x: ', dx, ' y: ', dy, 'surr: ', surr)
      if (surr > curr) {
        q.push([dx, dy])
        seen[dx][dy] = true
      }
    }
  }

  console.log('size', size)

  return size;
}

function solve(grid) {
  const sizes = []
  for (let i = 0; i < grid.length; i++) {
    for (let j = 0; j < grid[i].length; j++) {
      const size = basinSize(grid, i, j)
      sizes.push(size)
    }
  }
  sizes.sort((a, b) => b - a);

  console.log('sizes', sizes)
  return sizes[0] * sizes[1] * sizes[2]
}

main();