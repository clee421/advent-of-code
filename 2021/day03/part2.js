const fs = require('fs')

async function main() {
  const rawData = fs.readFileSync('./input-data', 'utf-8');
  const inputs = rawData.split('\n').map(d => {
    return d
  })

  const oxyGenRating = findOxyGenRating(inputs)
  const cO2ScrubRating = findCO2ScrubRating(inputs)

  console.log('oxyGenRating', oxyGenRating)
  console.log('cO2ScrubRating', cO2ScrubRating)
  console.log('rating', parseInt(oxyGenRating, 2) * parseInt(cO2ScrubRating, 2))
}

function findOxyGenRating(list) {
  for (let i = 0; i < list[0].length; i++) {
    const counter = countOnes(list)

    const half = list.length / 2
    let target = '1'
    if (counter[i] < half) {
      target = '0'
    }

    list = list.filter(t => t[i] === target)
    if (list.length === 1) {
      return list[0]
    }
  }

  throw new Error('hmmm')
}

function findCO2ScrubRating(list) {
  for (let i = 0; i < list[0].length; i++) {
    const counter = countOnes(list)

    const half = list.length / 2
    let target = '0'
    if (counter[i] < half) {
      target = '1'
    }

    list = list.filter(t => t[i] === target)
    if (list.length === 1) {
      return list[0]
    }
  }

  throw new Error('hmmm2')
}

function countOnes(list) {
  counter = Array.from({length: list[0].length}, (v, i) => 0)
  for (const bin of list) {
    for (let i = 0; i < bin.length; i++) {
      if (bin[i] === '1') {
        counter[i]++
      }
    }
  }
  
  return counter
}

main()