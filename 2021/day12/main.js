const fs = require('fs')

async function main() {
  const rawData = fs.readFileSync('./data-test3', 'utf-8');
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

function bfs2(start, graph) {
  // console.log('graph', graph)
  const paths = []
  const queue = [{
    currentPath: [start],
    seen: {},
  }]

  while (queue.length > 0) {
    const {currentPath, seen, parent} = queue.shift()

    const lastPosition = currentPath[currentPath.length - 1]

    if (lastPosition === 'end') {
      paths.push(currentPath.join(','))
      continue
    }

    let grandParent = null
    if (currentPath.length > 1) {
      grandParent = currentPath[currentPath.length - 2]
    }

    const children = graph[lastPosition] || []
    for (let i = 0; i < children.length; i++) {
      const child = children[i]
      const isLowercase = child.toLowerCase() === child

      // if (isLowercase && child === grandParent) {
      //   continue
      // }

      if (!seen[child] || seen[child] < 2) {
        const cloneSeen = {...seen}

        if (!cloneSeen[child]) {
          cloneSeen[child] = 0
        }

        if (isLowercase) {
          cloneSeen[child] += 1
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
