-- Copy to system clipboard
vim.keymap.set({"n", "v"}, "<leader>y", '"+y')

-- Paste from system clipboard
vim.keymap.set("n", "<leader>p", '"+p') 

-- Delete into black hole register
vim.keymap.set({"n", "v"}, "<leader>d", '"_d')
