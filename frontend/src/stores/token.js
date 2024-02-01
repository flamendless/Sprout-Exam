import { defineStore } from "pinia";

export const useTokenStore = defineStore("token", {
	state: () => {
		return {
			access_token: "",
			expires_in: "",
			refresh_token: "",
			token_type: "",
			type: "",
		}
	},
	persist: true,
});
