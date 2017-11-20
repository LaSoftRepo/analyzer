var settingsTmp =
    <div class="content-box-large">
        <div class="panel-heading">
            <div class="panel-title"><h4>Настройки</h4></div>
        </div>
        <br/>
        <br/>
        <br/>
        <br/>
        <div>
            <script type="text/ng-template" id="alert.html">
                <div ng-transclude></div>
            </script>
            <div uib-alert ng-repeat="alert in alerts" class="alert-info" close="closeAlert($index)">{{alert.msg}}</div>
        </div>
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
                        <div class="col-md-12">
                            <div class="form-group row">
                                <label class="col-sm-2 col-form-label"> Текст SMS</label>
                                <div class="col-sm-10">
                                    <textarea name="" id="" cols="" rows="5" ng-model="settings_site.message_text">ss</textarea>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-group row">
                                <label class="col-sm-2 col-form-label"> Вкл/выкл SMS</label>
                                <div class="col-sm-10">
                                    <input type="checkbox" value="{{settings_site.enable_disable_sms}}" class="custom-label" ng-checked="settings_site.enable_disable_sms" ng-model="settings_site.enable_disable_sms" />
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
                                <div class="checkbox" ng-repeat="site in status">
                                    <label><input type="checkbox" value="" class="custom-label" ng-checked="site.is_enable" ng-model="site.is_enable" />{{site.name}}</label>
                                </div>
                            </div>
                        </div>
                    </div>
                    <button type="button" class="btn btn-primary btn-sm float-right" ng-click="save_status()">Save</button>
                </div>
                <div class="col-md-6">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="row">
                                <div class="col-md-3">
                                    <input type="text" ng-model="word_input.word"/>
                                </div>
                                <div class="col-md-3">
                                    <button type="button" class="btn btn-primary btn-sm" ng-click="save_word()">Save</button>
                                </div>
                            </div>
                            <br/>

                             <ul class="list-group" style="max-width: 300px">
                                <li ng-repeat="word in stopwords" class="list-group-item d-flex justify-content-between align-items-center">{{word.word}}
                                    <div class="btn btn-danger badge badge-pill" ng-click="delete_word(word)">Delete</div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>;