var settingsTmp =
    <div class="content-box-large">
        <div class="panel-heading">
            <div class="panel-title"><h4>Настройки</h4></div>
        </div>
        <br/>
        <br/>
        <br/>
        <br/>
        <div class="panel-body">
            <div class="row container-fluid">
                <div class="col-md-3 right-column">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group row">
                                <label class="col-sm-2 col-form-label"> Цена, $</label>
                                <div class="col-sm-10">
                                    <input type="number" placeholder="От" ng-value="settings_site.price_usd_from" ng-model="settings_site.price_usd_from" />
                                    <input type="number" placeholder="До" ng-value="settings_site.price_usd_to" ng-model="settings_site.price_usd_to" />
                                </div>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-group row">
                                <label class="col-sm-2 col-form-label"> Цена, грн</label>
                                <div class="col-sm-10">
                                    <input type="number" placeholder="От" ng-value="settings_site.price_hrn_from" ng-model="settings_site.price_hrn_from" />
                                    <input type="number" placeholder="До" ng-value="settings_site.price_hrn_to" ng-model="settings_site.price_hrn_to" />
                                </div>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-group row">
                                <label class="col-sm-2 col-form-label"> Год</label>
                                <div class="col-sm-10">
                                    <input type="text" placeholder="От" class="datepicker-plugin" ng-value="settings_site.date_from" ng-model="settings_site.date_from" />
                                    <input type="text" placeholder="До" class="datepicker-plugin" ng-value="settings_site.date_to" ng-model="settings_site.date_to" />
                                </div>
                            </div>
                        </div>
                    </div>
                    <button type="button" class="btn btn-primary btn-sm float-right" ng-click="save_settings()">Save</button>
                </div>
                <div class="col-md-3 right-column">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group">
                                <div class="checkbox">
                                    <label><input type="checkbox" value="" class="custom-label">Option 1</label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button type="button" class="btn btn-primary btn-sm float-right">Save</button>
                </div>
                <div class="col-md-6">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="row">
                                <div class="col-md-3">
                                    <input type="text"/>
                                </div>
                                <div class="col-md-3">
                                    <button type="button" class="btn btn-primary btn-sm">Save</button>
                                </div>
                            </div>
                            <br/>

                             <ul class="list-group">
                                <li class="list-group-item d-flex justify-content-between align-items-center">First item <div class="btn btn-danger badge badge-pill">Delete</div></li>
                                <li class="list-group-item">Second item</li>
                                <li class="list-group-item">Third item</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>;