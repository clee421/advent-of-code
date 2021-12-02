const fs = require('fs')
async function main() {
  const rawData = fs.readFileSync('./input-data', 'utf-8');
  const inputs = rawData.split('\n').map(d => {
    return parseInt(d.trim())
  })
  let count = 0
  for (let i = 1; i < inputs.length; i++) {
    if (inputs[i-1] < inputs[i]) {
      count++
    }
  }
  console.log('count', count)
}
main()
