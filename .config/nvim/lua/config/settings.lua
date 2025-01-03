vim.opt.termguicolors = true

-- Open telescope when opening nvim with a directory as parameter
vim.api.nvim_create_autocmd("VimEnter", {
  callback = function()
    local first_argument = vim.fn.argv(0)
    if vim.fn.isdirectory(first_argument) ~= 0 then
      vim.api.nvim_command(":cd " .. first_argument)
      require("telescope.builtin").find_files()
    end
  end,
})

-- Auto update lazy when entering nvim
vim.api.nvim_create_autocmd("VimEnter", {
  callback = function()
    require("lazy").update({
      show = false,
    })
  end
})

vim.opt.background = "light"
vim.cmd('hi Normal guibg=#f3f4f9e6') -- e6 = 90% opacity
