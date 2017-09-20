var adminTmp =
    <div class="content-box-large">
    <div class="panel-heading">
       <div class="panel-title"><h4>Administrators</h4></div>
       <a href="#!/admin/create" class="btn btn-primary" style="float: right; margin-bottom: 10px;">Add</a>
    </div>
    <div class="panel-body">
       <div class="table-responsive">
           <table class="table">
              <thead>
                   <tr>
                       <th>ID</th>
                       <th>First Name</th>
                       <th>Last Name</th>
                      <th>Username</th>
                       <th>Email</th>
                   </tr>
               </thead>
               <tbody>
                  <tr ng-repeat="user in users">
                       <td>{{user.id}}</td>
                       <td>{{user.first_name}}</td>
                       <td>{{user.last_name}}</td>
                      <td>{{user.username}}</td>
                       <td>{{user.email}}</td>
                   </tr>
               </tbody>
           </table>
       </div>
       <nav ng-if="users_count > 10">
           <ul class="pagination">
               <li class="page-item" ng-class="{active: current_page == pages}" ng-repeat="pages in count_paginator(total_pages)">
                   <a class="page-link" href="" ng-click="get_users(pages)">{{pages}}</a>
               </li>
           </ul>
       </nav>
    </div>;

var adminCreateTmp =
    <div class="content-box-large">
    <div class="panel-heading">
       <div class="panel-title"><h4>Create User</h4></div>
       <a href="#!admin" class="btn btn-primary" style="float: right; margin-bottom: 10px;">Return</a>
    </div>
    <div class="panel-body">
    <div class="table-responsive">
    <div class="form-group row">
       <div class="col-9">
           <input ng-model="user.first_name" class="form-control" type="text" placeholder="First Name" id="example-text-input" />
       </div>
    </div>
    <div class="form-group row">
       <div class="col-9">
           <input ng-model="user.last_name" class="form-control" type="text" placeholder="Second Name" id="example-text-input" />
       </div>
    </div>
    <div class="form-group row">
       <div class="col-9">
           <i class="text-danger" ng-if="error_username">{{error_username}}</i>
           <input ng-model="user.username" class="form-control" type="text" placeholder="Username" id="example-text-input" />
       </div>
    </div>
    <div class="form-group row">
       <div class="col-9">
           <i class="text-danger" ng-if="error_email">{{error_email}}</i>
           <input ng-model="user.email" class="form-control" type="text" placeholder="Email" id="example-text-input" />
       </div>
    </div>
    <div class="form-group row">
       <div class="col-9">
           <i class="text-danger" ng-if="error_password">{{error_password}}</i>
           <input ng-model="user.password" class="form-control" type="text" placeholder="Password" id="example-text-input" />
       </div>
    </div>
    <div class="form-group row">
       <div class="col-9">
           <i class="text-danger" ng-if="error_password || error_password2"> {{error_password || error_password2}} </i>
           <input ng-model="user.password2" class="form-control" type="text" placeholder="Confirm Password" id="example-text-input" />
       </div>
    </div>
        <input ng-click="save()" type="submit" value="Save" class="btn btn-success" />
    </div>
    </div>;
