vim.opt.termguicolors = true

vim.api.nvim_create_autocmd("VimEnter", {
  callback = function()
    local first_argument = vim.fn.argv(0)
    if vim.fn.isdirectory(first_argument) ~= 0 then
      vim.api.nvim_command(":cd " .. first_argument)
      require("telescope.builtin").find_files()
    end
  end,
})

vim.opt.background = "light"
vim.cmd('hi Normal guibg=#f3f4f9')

-- vim.api.nvim_command([[
--     augroup ChangeBackgroudColour
--         autocmd colorscheme * :hi normal guibg=#f3f4f9
--     augroup END
-- ]])
