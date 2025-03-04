<script>
import axios from "axios";

export default{
  data() {
    return {
      message: "",
    };
  },
  mounted() {
    axios
      .get("http://localhost:5000/test-api")  // Ensure the URL is correct
      .then((response) => {
        console.log("Response received:", response.data);
        this.message = response.data.message; // Store API data
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  },
};

</script>

<template>
  <div>
    <h1>Admin Page</h1>
    <p>API Response: {{ message }}</p>
  </div>
</template>

<style scoped>

</style>
