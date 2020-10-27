import _ from "lodash";

async function executeFunction(data: any): Promise<any> {
  let splitSequenceX: Array<Array<number>> = [[]];
  let splitSequenceY: Array<number> = [];

  let dataLen: number = data.sequence.length;
  let steps: number = data.steps;
  let iterations = 0;

  while (dataLen > steps) {
    console.log(dataLen);
    splitSequenceX.push(_.slice(data.sequence, 0, steps));
    splitSequenceY.push(data.sequence[steps]);
    data.sequence = _.drop(data.sequence);
    dataLen = data.sequence.length;
    iterations = iterations + 1;
  }
  splitSequenceX = _.drop(splitSequenceX);

  return Promise.resolve({
    length: dataLen,
    iterations: iterations,
    splitSequenceX: splitSequenceX,
    splitSequenceY: splitSequenceY,
  });
}
