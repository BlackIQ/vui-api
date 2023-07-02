const input = {
  services: ["coffee", "restaurant", "sbbiran", "root", "ssms"],
  positions: [6, 7, 8, 9],
  slugs: [1, 2, 3, 4, 5],
  states: ["Tehran", "Shiraz", "Qarchak", "Varamin"],
  dates: ["2023/01/01", "2023/01/05"],
  name: "John Doe",
};

const startDate = new Date(input.dates[0]);
const endDate = new Date(input.dates[1]);

const output = [];

for (const service of input.services) {
  for (const position of input.positions) {
    for (const slug of input.slugs) {
      for (const state of input.states) {
        let currentDate = new Date(startDate);

        while (currentDate <= endDate) {
          output.push({
            service,
            position,
            slug,
            state,
            date: currentDate.toLocaleDateString(),
            name: input.name,
          });

          currentDate.setDate(currentDate.getDate() + 1);
        }
      }
    }
  }
}

console.log(output);
console.log(output.length);
