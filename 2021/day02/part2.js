const fs = require('fs')
 async function main() {
   const rawData = fs.readFileSync('./input-data', 'utf-8');
   const inputs = rawData.split('\n').map(d => {
     const [direction, rawDistance] = d.split(' ')
     return {direction, value: parseInt(rawDistance)}
   })
   let [horizontal, depth, aim] = [0, 0, 0]
   for (const instruct of inputs) {
     switch (instruct.direction) {
       case 'forward':
         horizontal += instruct.value
         depth += (aim * instruct.value)
         break;
       case 'down':
         aim += instruct.value
         break;
       case 'up':
         aim -= instruct.value
         break;
       default:
         throw new Error(`wtf is ${instruct.direction}`)
     }
   }
   console.log('horizontal', horizontal)
   console.log('depth', depth)
   console.log('dist', horizontal * depth)
 }
 main()
