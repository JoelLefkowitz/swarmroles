function quit(name) {
  console.log("Task: '".concat(name, "' has not been implemented"));
}

module.exports = function (grunt) {
  grunt.initConfig();
  grunt.registerTask("run", (env) => quit("run"));
  grunt.registerTask("build", (env) => quit("build"));
  grunt.registerTask("tests", (target) => quit("tests"));
  grunt.registerTask("docs", (target) => quit("docs"));
  grunt.registerTask("lint", () => quit("lint"));
  grunt.registerTask("format", () => quit("format"));
  grunt.registerTask("precommit", [
    "lint",
    "format",
    "tests:coverage",
    "docs:generate",
  ]);
};
