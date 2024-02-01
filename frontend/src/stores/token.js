import { ref } from "vue";
import { defineStore } from "pinia";

export const useTokenStore = defineStore("token", () => {
	const access_token = ref("");
	const expires_in = ref(0);
	const refresh_token = ref("");
	const token_type = ref("");
	const type = ref("");

	return {
		access_token,
		expires_in,
		refresh_token,
		token_type,
		type
	};
});
