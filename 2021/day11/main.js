const fs = require('fs')

const DELTAS = [
  // left
  {x: 0, y: -1},
  // up
  {x: -1, y: 0},
  // down
  {x: 1, y: 0},
  // right
  {x: 0, y: 1},
  // up left
  {x: -1, y: -1},
  // up right
  {x: -1, y: 1},
  // down right
  {x: 1, y: 1},
  // down left
  {x: 1, y: -1},
]

async function main() {
  const rawData = fs.readFileSync('./data-input', 'utf-8');
  const inputs = rawData.split('\n').map(d => {
    return d.trim()
  })

  const grid = parse(inputs)
  // const score = solve(grid)
  const step = solve2(grid)

  console.log('step', step)
}

function solve(grid) {
  let flashes = 0;

  for (let s = 0; s < 100; s++) {
    const count = takeStep(grid)
    flashes += count

    // grid.render()
  }

  return flashes;
}

function solve2(grid) {
  let steps = 1
  while (true) {
    const count = takeStep(grid);
    // console.log('count', count)
    if (count === grid.size()) {
      return steps;
    }

    steps++
  }

  return -1;
}

function takeStep(grid) {
  const flashed = []
  grid.grid.forEach(r => flashed.push(new Array(r.length).fill(false)))

  grid.gainEnergy(1)

  const flashersQ = []
  for (let i = 0; i < grid.grid.length; i++) {
    for (let j = 0; j< grid.grid[i].length; j++) {
      flashersQ.push({x: i, y: j })

      while (flashersQ.length > 0) {
        const {x, y} = flashersQ.shift()
        // console.log(`x: ${x}, y: ${y}`)
        const octo = grid.grid[x][y]
        if (!flashed[x][y] && octo.shouldFlash()) {
          flashed[x][y] = true

          const adj = grid.getSurround(x, y)
          // console.log('adj', adj)
          adj.forEach((a) => {
            // console.log(`ax: ${a.x}, ay: ${a.y}`)
            grid.grid[a.x][a.y].gainEnergy(1)
          })

          flashersQ.push(...adj)
        }
      }
    }
  }

  let max = 0;
  let flashes = 0;
  for (let i = 0; i < flashed.length; i++) {
    for (let j = 0; j< flashed[i].length; j++) {
      max++
      if (flashed[i][j]) {
        grid.grid[i][j].flash()
        flashes++
      }
    }
  }

  return flashes;
}

function parse(lines) {
  const grid = new Grid();
  lines.forEach(l => grid.add(l))

  return grid
}

class Grid {
  constructor() {
    this.sizeVar = 0;
    this.grid = []
  }

  // row - string
  add(row) {
    const newRow = row.split('').map(c => new Octopus(parseInt(c)));
    this.sizeVar += newRow.length
    this.grid.push(newRow)
  }

  size() {
    return this.sizeVar
  }

  getSurround(x, y) {
    // console.log(`getSurround; x: ${x}, y: ${y}`)
    const surround = []

    for (let i = 0; i < DELTAS.length; i++) {
      const d = DELTAS[i]
      // console.log(`i ${i} - ${d.x},${d.y}`)
      const nx = d.x + x
      const ny = d.y + y

      // console.log(`nx: ${nx}, ny: ${ny}`)
      if (nx < 0 || nx >= this.grid.length) {
        continue;
      }

      if (ny < 0 || ny >= this.grid[nx].length) {
        continue;
      }

      if (this.grid[nx][ny] > 9) {
        continue;
      }

      surround.push({x: nx, y: ny})
    }

    return surround
  }

  gainEnergy(level) {
    for (let i = 0; i < this.grid.length; i++) {
      for (let j = 0; j < this.grid[i].length; j++) {
        // console.log(this.grid[i][j])
        this.grid[i][j].gainEnergy(level)
      }
    }
  }

  render() {
    const rows = []
    for (let i = 0; i < this.grid.length; i++) {
      const row = []
      for (let j = 0; j< this.grid[i].length; j++) {
        row.push(this.grid[i][j].energy === 0 ? '*' : this.grid[i][j].toString())
      }
      rows.push(row.join(''))
    }

    console.log(rows.join('\n'))
  }
}

class Octopus {
  constructor(energy) {
    this.energy = energy;
  }

  shouldFlash() {
    return this.energy > 9
  }

  flash() {
    if (!this.shouldFlash()) {
      throw new Error('should not be flashing')
    }

    this.energy = 0
  }

  gainEnergy(level) {
    this.energy += level
  }

  toString() {
    return this.energy.toString();
  }
}

main()
