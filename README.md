# lmarena-history

JSONized [lmarena.ai](https://lmarena.ai) score data.

## Where

JSON data is on https://github.com/nakasyou/lmarena-history/blob/main/output/scores.json.

## What

```ts
// JSON Data
type Data = {
  [yyyymmdd: `${number}`]: {
    text: Columns // conversations which uses only text
    vision?: Columns // conversations using a vision model
  }
}

/**
 * Including `overall`, `japanese`, `math`, `coding`, and more...
 */
type Columns = Record<string, Score>

type Score = {
  [modelID: string]: number // elo score
}
```

## How

lmarena manages that data in [HuggingFace](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard/tree/main). The data is saved as Python Pickle file. The project uses GitHub Actions to process data.

## When

The data is updated every day by GitHub Actions.

## Why

As I wrote original data is saved as Python Pikcle file, so it's diffucult to use it with other languages. By converting to JSON, you can use the data using other languages such as JavaScript.
