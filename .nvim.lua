vim.keymap.set("n", "<leader>b", function()
	vim.fn.jobstart({
		"python",
		vim.fn.expand("%:p"),
	}, {
		stdout_buffered = true,
		on_stdout = function(_, data)
			if data then
				vim.notify(table.concat(data, "\n"))
			end
		end,
		on_stderr = function(_, data)
			if data then
				vim.notify(table.concat(data, "\n"), vim.log.levels.ERROR)
			end
		end,
	})
end, { desc = "[B]uild Project" })
