/** @odoo-module **/
import { Component, tags, mount } from 'owl';

class MyComponent extends Component {
    static template = tags.xml/* xml */ `
        <div>
            <h1>Welcome to DRV Printing</h1>
        </div>
    `;
}

mount(MyComponent, document.getElementById('my_component'));
