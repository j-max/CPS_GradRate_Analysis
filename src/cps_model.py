import sklearn.pipeline
from sklearn.model_selection import cross_val_predict, cross_validate
from sklearn.metrics import mean_squared_error, r2_score

def cv_cps(model, X_train, y_train, features):

    """Given a model and a set of features
    print out the train and test scores from validation.

    Also, refit to entire dataset, and print out coefficients
    """

    cv_fsm = cross_validate(model, X_train[features], y_train, cv=4, return_train_score=True)
    print('Train Scores')
    print(cv_fsm['train_score'])
    print(cv_fsm['train_score'].mean())
    print(cv_fsm['train_score'].std())
    print('##########################')
    print('Test Scores')
    print(cv_fsm['test_score'])
    print(cv_fsm['test_score'].mean())
    print(cv_fsm['test_score'].std())
    print('##########################')

    if type(model) != sklearn.pipeline.Pipeline:
        model.fit(X_train[features], y_train)
        print('Coefficients from fit on full train set')
        print(model.coef_, model.intercept_)




def print_cv_results(model, X_train, features_list, y_train):
    
    cv_fsm = cross_validate(model, X_train[features_list], y_train, cv=3, 
                        return_train_score=True, scoring=['neg_root_mean_squared_error', 'r2'])

    
    print('#####r2#####')

    print(cv_fsm['train_r2'].mean())
    print('test')
    print(cv_fsm['test_r2'])
    print(cv_fsm['test_r2'].mean())
    print('#####rmse#####')
    print("#####Train####")
    print(-cv_fsm['train_neg_root_mean_squared_error'])
    print(-cv_fsm['train_neg_root_mean_squared_error'].mean())
    print('test')
    print(-cv_fsm['test_neg_root_mean_squared_error'])
    print(-cv_fsm['test_neg_root_mean_squared_error'].mean())
    
    
    # Cross Val Predict
    print('cross val predict metrics: test scores')
    y_hat = cross_val_predict(model, X_train[features_list], y_train, cv=3)
    
    rmse = mean_squared_error(y_train, y_hat, squared=False)
    '''As stated in the docs, these numbers are a bit different 
    most likely because of different test sizes in each fold'''
    
    print("RMSE")
    print(rmse)
    
    r2 = r2_score(y_train, y_hat)
    print("r2")

    print(r2)
    
    return cross_val_predict(model, X_train[features_list], y_train, cv=3)