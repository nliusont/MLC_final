# perform randomized grid search to find the parameters

#parameters to search
param_dist = {'max_features': list(range(20,31,1)),
             'max_depth':list(range(16,28,1)),
            'n_estimators': [500, 600, 700]}

# three-fold CV across 30 cores, 60 iterations per run
pre_gs_inst = RandomizedSearchCV(ExtraTreesRegressor(min_samples_leaf = 4, min_samples_split = 2),
            param_distributions = param_dist,
            cv=3,
            n_jobs=30,
            n_iter=60)

pre_gs_inst.fit(X_train, y_train.values.ravel())
print(pre_gs_inst.best_params_)

y_pre_gs = pre_gs_inst.predict(X_test)
r2 = r2_score(y_test, y_pre_gs)
print(r2)
