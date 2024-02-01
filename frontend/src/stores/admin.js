import { defineStore } from "pinia";


export const useAdminStore = defineStore("admin", {
	state: () => ({
		data: [],
		layout: "grid",
	}),

	actions: {
		toggle_layout() {
			if (this.layout == "grid") {
				this.layout = "list";
			} else if (this.layout == "list") {
				this.layout = "grid";
			}
		}
	},
});
