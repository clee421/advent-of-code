const { count } = require('console');
const fs = require('fs')

async function main() {
  const rawData = fs.readFileSync('./data-test', 'utf-8');
  const inputs = rawData.split('\n').map(d => {
    return d.trim()
  })

  const grid = parse(inputs)
  const ans = solve(grid)
  // const ans = solve2(data)

  console.log('ans', ans)
}

function solve(grid) {
  // test cases
  // fold along y=7
  // fold along x=5

  // input cases
  // fold along x=655
  // fold along y=447
  // fold along x=327
  // fold along y=223
  // fold along x=163
  // fold along y=111
  // fold along x=81
  // fold along y=55
  // fold along x=40
  // fold along y=27
  // fold along y=13
  // fold along y=6
  grid.horizontalFold(655)
  grid.render()

  return grid.count();
}

function solve2(grid) {
  return -1;
}

function parse(lines) {
  const grid = new Grid()
  lines.forEach((line) => {
    const [l, r] = line.split(',')
    const x = parseInt(l)
    const y = parseInt(r)

    grid.add(y, x)
  })

  // grid.render()
  return grid
}

class Grid {
  constructor() {
    // test cases
    // const X_LIMIT = 15
    // const Y_LIMIT = 11

    // input cases
    const X_LIMIT = 890
    const Y_LIMIT = 1311;

    this.grid = new Array(X_LIMIT)
    this.maxX = 0
    this.maxY = 0

    for (let i = 0; i < X_LIMIT; i++) {
      this.grid[i] = new Array(Y_LIMIT).fill(false)
    }
  }

  add(x, y) {
    this.grid[x][y] = true
  }

  horizontalFold(index) {
    const top = []
    const bottom = []
    for (let i = 0; i < index; i++) {
      top.push(this.grid[i])
    }

    for (let i = index+1; i < this.grid.length; i++) {
      bottom.unshift(this.grid[i])
    }

    if (top.length !== bottom.length) {
      throw new Error(`top(size: ${top.length}) and bottom(size: ${bottom.length}) sizes do not match`)
    }

    const merged = []
    for (let i = 0; i < top.length; i++) {
      const row = new Array(top[i].length).fill(false)
      for (let j = 0; j < top[i].length; j++) {
        row[j] = top[i][j] || bottom[i][j]
      }

      merged.push(row)
    }

    this.grid = merged
  }

  count() {
    let count = 0
    for (let i = 0; i < this.grid.length; i++) {
      for (let j = 0; j < this.grid[i].length; j++) {
        if (this.grid[i][j]) {
          count++
        }
      }
    }

    return count;
  }

  render() {
    for (let i = 0; i < this.grid.length; i++) {
      const row = []
      for (let j = 0; j < this.grid[i].length; j++) {
        row.push(this.grid[i][j] ? '#' : '.')
      }

      console.log(row.join(''))
    }
  }
}

main()