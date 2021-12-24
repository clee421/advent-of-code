const fs = require('fs')

async function main() {
  const rawData = fs.readFileSync('./data-input', 'utf-8');
  const inputs = rawData.split('\n').map(d => {
    return d.trim()
  })

  const graph = parse(inputs)
  // console.log('graph', graph)
  const count = solve(graph)

  console.log('count', count)
}

function solve(graph) {
  // const result = dfs('start', graph)
  const result = bfs2('start', graph)
  console.log(result)

  return result.length
}

function bfs(start, graph) {
  // console.log('graph', graph)
  const paths = []
  const queue = [{
    currentPath: [start],
    seen: {},
    // parent: null,
  }]

  while (queue.length > 0) {
    const {currentPath, seen, parent} = queue.shift()
    // console.log('currentPath', currentPath)

    const lastPosition = currentPath[currentPath.length - 1]

    if (lastPosition === 'end') {
      paths.push(currentPath.join(','))
      continue
    }

    const children = graph[lastPosition] || []
    for (let i = 0; i < children.length; i++) {
      const child = children[i]
      const isLowercase = child.toLowerCase() === child

      if (!seen[child]) {
        const cloneSeen = {...seen}

        if (isLowercase) {
          cloneSeen[child] = true
        }

        queue.push({
          currentPath: [...currentPath, child],
          seen: cloneSeen,
          // parent: lastPosition,
        })
      }
    }
  }

  return paths
}

/**
 * Part two is poorly explained. Why is start,A,b,d,b,A,c,A,c,A,end not an accepted path?
 * It fits all criterias of the problem:
 * Distince path from start to end
 * Visits the large caves a limitless number of times
 * Visits the small cave at most twice
 *
 * Saw a post on reddit
 * https://www.reddit.com/r/adventofcode/comments/rehj2r/comment/hpunqyk/?utm_source=share&utm_medium=web2x&context=3
 *
 * you can visit ONE cave at most twice. fuck you AOC
 */
function bfs2(start, graph) {
  // console.log('graph', graph)
  const paths = []
  const queue = [{
    currentPath: [start],
    seen: {},
  }]

  let iterations = 0
  let mods = 1000
  while (queue.length > 0) {
    const {currentPath, seen, twiceSeen} = queue.shift()

    const lastPosition = currentPath[currentPath.length - 1]

    if (lastPosition === 'end') {
      paths.push(currentPath.join(','))
      continue
    }

    if (iterations % mods === 0) {
      if (iterations > mods * 10) {
        mods *= 10
      }
      console.log(iterations, 'currentPath', currentPath.join('-'))
    }

    const children = graph[lastPosition] || []
    for (let i = 0; i < children.length; i++) {
      let haveSeenTwice = twiceSeen ?? false;
      const child = children[i]
      const isLowercase = child.toLowerCase() === child

      if (!seen[child] || (!twiceSeen && seen[child] < 2)) {
        const cloneSeen = {...seen}

        if (!cloneSeen[child]) {
          cloneSeen[child] = 0
        }

        if (isLowercase) {
          cloneSeen[child] += 1
          if (cloneSeen[child] > 1) {
            // console.log('hmmm')
            haveSeenTwice = true
          }
        }

        queue.push({
          currentPath: [...currentPath, child],
          seen: cloneSeen,
          twiceSeen: haveSeenTwice,
        })
      }
    }

    iterations++
  }

  return paths
}

function parse(lines) {
  const graph = {}
  lines.forEach(l => {
    const [start, end] = l.split('-')
    if (!graph[start]) {
      graph[start] = []
    }

    if (!graph[end]) {
      graph[end] = []
    }

    if (end !== 'start') {
      graph[start].push(end)
    }
    if (start !== 'start') {
      graph[end].push(start)
    }
  })

  delete graph['end']

  return graph
}


main()
