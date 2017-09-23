var parserTmp =
'    <div class="content-box-large">'+
'        <div class="panel-heading">'+
'            <div class="panel-title"><h3>Объявления</h3></div>'+
'        </div>'+
'        <div class="panel-body">'+
'            <table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="example">'+
'                <thead>'+
'                    <tr>'+
'                        <th>Дата</th>'+
'                        <th>Время</th>'+
'                        <th>Сайт</th>'+
'                        <th>ID на сайте</th>'+
'                        <th>Город</th>'+
'                        <th>Заголовок</th>'+
'                        <th>Описание</th>'+
'                        <th>Ссылка</th>'+
'                        <th>Цена</th>'+
'                        <th>Телефон</th>'+
'                        <th>Имя</th>'+
'                        <th>СМС</th>'+
'                        <th>Email</th>'+
'                    </tr>'+
'                </thead>'+
'                <tbody>'+
'                    <tr class="odd gradeX" ng-repeat="collection in collections">'+
'                        <td>{{collection.create_at | date:"yyyy-MM-dd"}}</td>'+
'                        <td>{{collection.create_at | date:"HH:mm"}}</td>'+
'                        <td>{{collection.donor}}</td>'+
'                        <td class="center">{{collection.id_donor}}</td>'+
'                        <td class="center">{{collection.city}}</td>'+
'                        <td class="center">{{collection.title}}</td>'+
'                        <td class="center">{{collection.description}}</td>'+
'                        <td class="center"><a href="{{collection.link}}">LINK</a></td>'+
'                        <td class="center">{{collection.price}}</td>'+
'                        <td class="center">{{collection.phones}}</td>'+
'                        <td class="center">{{collection.name}}</td>'+
'                        <td class="center">{{collection.sms_is_send}}</td>'+
'                        <td class="center">{{collection.email_is_send}}</td>'+
'                    </tr>'+
'                </tbody>'+
'            </table>'+
'        </div>'+
'        <nav ng-if="collection_count > 10">'+
'           <ul class="pagination">'+
'               <li class="page-item" ng-class="{active: current_page == pages}" ng-repeat="pages in count_paginator(total_pages)">'+
'                   <a class="page-link" href="" ng-click="get_collection(pages)">{{pages}}</a>'+
'               </li>'+
'           </ul>'+
'       </nav>'+
'    </div>';
