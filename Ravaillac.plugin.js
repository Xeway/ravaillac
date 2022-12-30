module.exports = class Ravaillac {
    start() {
      // Called when the plugin is activated (including after reloads)
      BdApi.alert("Hello World!", "This is my first plugin!");
    }

    stop() {
      // Called when the plugin is deactivated
    }
}
