import React, { Component } from "react";

class Depth extends Component {
  render() {
    return (
      <div className="form-group">
        <input
          type="number"
          value={this.props.value}
          onChange={e => this.props.onChange(e)}
          className="form-control col-2"
          placeholder="Depth"
        />
      </div>
    );
  }
}

export default Depth;
