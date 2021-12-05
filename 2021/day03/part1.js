const fs = require('fs')

async function main() {
  const rawData = fs.readFileSync('./input-data', 'utf-8');
  const inputs = rawData.split('\n').map(d => {
    return d
  })

  const counter = Array.from({length: inputs[0].length}, (v, i) => 0)
  for (const bin of inputs) {
    for (let i = 0; i < bin.length; i++) {
      if (bin[i] === '1') {
        counter[i]++
      }
    }
  }

  let gamma = ''
  let epsilon = ''
  let half = inputs.length / 2
  for (const c of counter) {
    if (c > half) {
      gamma += '1'
      epsilon += '0'
    } else {
      gamma += '0'
      epsilon += '1'
    }
  }

  console.log('gamma', gamma)
  console.log('epsilon', epsilon)
  console.log('power', parseInt(gamma, 2) * parseInt(epsilon, 2))
}

main()