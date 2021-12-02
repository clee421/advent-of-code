const fs = require('fs')
async function main() {
  const rawData = fs.readFileSync('./input-data', 'utf-8');
  const inputs = rawData.split('\n').map(d => {
    return parseInt(d.trim())
  })
  let curr = inputs[0] + inputs[1] + inputs[2]
  let count = 0
  for (let i = 3; i < inputs.length; i++) {
    const prev = curr;
    curr = curr + inputs[i] - inputs[i-3]
    if (prev < curr) {
      count++
    }
  }
  console.log('count', count)
}
main()
