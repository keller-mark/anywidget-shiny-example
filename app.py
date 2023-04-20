from shiny import App, render, ui
from shinywidgets import output_widget, render_widget

import anywidget
import traitlets

class CounterWidget(anywidget.AnyWidget):
    # Widget front-end JavaScript code
    _esm = """
    export function render(view) {
      let getCount = () => view.model.get("count");
      let button = document.createElement("button");
      button.innerHTML = `count is ${getCount()}`;
      button.addEventListener("click", () => {
        view.model.set("count", getCount() + 1);
        view.model.save_changes();
      });
      view.model.on("change:count", () => {
        button.innerHTML = `count is ${getCount()}`;
      });
      view.el.appendChild(button);
    }
    """
    # Stateful property that can be accessed by JavaScript & Python
    count = traitlets.Int(0).tag(sync=True)

app_ui = ui.page_fluid(
    ui.h2("Hello Shiny!"),
    output_widget("my_widget"),
)


def server(input, output, session):
    @output
    @render_widget
    def my_widget():
        return CounterWidget()


app = App(app_ui, server)
