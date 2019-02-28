import React, { Component } from "react";

class Url extends Component {
  render() {
    return (
      <div className="form-group">
        <input
          type="text"
          value={this.props.value}
          onChange={e => this.props.onChange(e)}
          className="form-control col-4"
          placeholder="URL"
        />
      </div>
    );
  }
}

export default Url;
