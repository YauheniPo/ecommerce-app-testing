"use strict"

process.env.LOG_TO_STDERR = process.env.LOG_TO_STDERR || "true"
process.env.LOG_LEVEL = process.env.LOG_LEVEL || "error"
process.env.NO_COLOR = process.env.NO_COLOR || "1"

const path = require("node:path")
const { createRequire } = require("node:module")
const requireFromRegister = createRequire(__filename)
const threadStreamRoot = path.dirname(
  requireFromRegister.resolve("thread-stream/package.json"),
)
globalThis.__bundlerPathsOverrides = {
  "thread-stream-worker": path.join(threadStreamRoot, "lib", "worker.js"),
}

const dotenv = require("dotenv")

const root = path.resolve(__dirname, "..")
dotenv.config({ path: path.join(root, ".env") })
if (process.env.API_KEY && !process.env.OBSIDIAN_API_KEY) {
  process.env.OBSIDIAN_API_KEY = process.env.API_KEY
}
if (process.env.OBSIDIAN_REST_API_KEY && !process.env.OBSIDIAN_API_KEY) {
  process.env.OBSIDIAN_API_KEY = process.env.OBSIDIAN_REST_API_KEY
}
if (process.env.OBSIDIAN_API_URL && !process.env.OBSIDIAN_BASE_URL) {
  process.env.OBSIDIAN_BASE_URL = process.env.OBSIDIAN_API_URL
}
