const fs = require('fs')

const OPEN = {
  '(': ')',
  '[': ']',
  '{': '}',
  '<': '>',
}

const CLOSE = {
  ')': '(',
  ']': '[',
  '}': '{',
  '>': '<',
}

const POINTS = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137,
}

const POINTS2 = {
  ')': 1,
  ']': 2,
  '}': 3,
  '>': 4,
}

async function main() {
  const rawData = fs.readFileSync('./data-input', 'utf-8');
  const inputs = rawData.split('\n').map(d => {
    return new Line(d.trim())
  })

  const score = solve2(inputs)

  console.log('score', score)
}

function solve(lines) {
  let score = 0;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].isCorrupt()) {
      score += lines[i].score('corrupt')
    }
  }

  return score;
}

function solve2(lines) {
  let score = [];
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].isIncomplete()) {
      score.push(lines[i].score('incomplete'))
    }
  }

  score.sort((a, b) => a - b);
  const mid = Math.floor(score.length / 2)
  return score[mid];
}

class Line {
  constructor(line) {
    this.line = line;
    this.illegalChar = '';
    this.missingChars = [];
  }

  isCorrupt() {
    if (this.illegalChar) {
      return true
    }

    const stack = [];
    for (let i = 0; i < this.line.length; i++) {
      if (OPEN[this.line[i]]) {
        stack.push(this.line[i])
      } else if (CLOSE[this.line[i]]) {
        const open = CLOSE[this.line[i]]
        const peekOpen = stack[stack.length-1]
        if (peekOpen !== open) {
          this.illegalChar = this.line[i]
          return true
        } else {
          stack.pop()
        }
      }
    }

    return false;
  }

  isIncomplete() {
    if (this.isCorrupt()) {
      return false
    }

    if (this.missingChars.length > 0) {
      return true;
    }

    const stack = [];
    for (let i = 0; i < this.line.length; i++) {
      if (OPEN[this.line[i]]) {
        stack.push(this.line[i])
      } else if (CLOSE[this.line[i]]) {
        const open = CLOSE[this.line[i]]
        const peekOpen = stack[stack.length-1]
        if (peekOpen === open) {
          stack.pop()
        }
      }
    }

    while (stack.length > 0) {
      const next = stack.pop();
      this.missingChars.push(OPEN[next])
    }

    return this.missingChars.length > 0
  }

  score(type) {
    if (type === 'corrupt' && this.isCorrupt()) {
      return POINTS[this.illegalChar]
    }

    if (type === 'incomplete') {
      // console.log('nani')
      let points = 0;
      for (let i = 0; i < this.missingChars.length; i++) {
        points *= 5
        points += POINTS2[this.missingChars[i]]
      }

      // console.log('points', points)
      return points;
    }

    return 0
  }
}

main()
