return {
  {
    "NvChad/nvim-colorizer.lua",
    opts = {},
    version = false,
  },
  {
    "kylechui/nvim-surround",
    version = "*", -- Use for stability; omit to use `main` branch for the latest features
    event = "VeryLazy",
    config = function()
        require("nvim-surround").setup({
            -- Configuration here, or leave empty to use defaults
        })
    end
  },
  {
    "nvim-telescope/telescope.nvim",
    tag = "0.1.8",
    dependencies = { "nvim-lua/plenary.nvim" },
    keys = {
      { "<leader>ff", function() require("telescope.builtin").find_files() end, desc="[f]ind [f]iles" },
      { "<leader>fg", function() require("telescope.builtin").live_grep() end, desc="Live [g]rep" },
    },
  },
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function () 
      local configs = require("nvim-treesitter.configs")

      configs.setup({
          ensure_installed = { "c", "lua", "vim", "vimdoc", "query", "elixir", "heex", "javascript", "html", "haskell" },
          sync_install = false,
          highlight = { enable = true },
          indent = { enable = true },  
        })
    end
  },
  {
    "williamboman/mason.nvim",
    opts = {
      ensure_installed = {
        "haskell-language-server"	
      },
    },
    config = function()
      require("mason").setup({
      })
    end
  },
  {
    "neovim/nvim-lspconfig",
    dependencies = {
      "williamboman/mason.nvim",
    },
    config = function()
      local lspconfig = require("lspconfig")
      local mason = require("mason")
	
      mason.setup()
      lspconfig.rust_analyzer.setup({})
      lspconfig.hls.setup({})
    end
  },
  {
    "nvim-lua/lsp-status.nvim",
	
  }
}
