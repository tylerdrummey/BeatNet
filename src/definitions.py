
torch.manual_seed(48) #For training consistency
class DataPrepPipeline:
    """
    Data Preparation pipeline for the compatibility model.
    """
    def __init__(self):
      pass

    def transform(self, X):
      #drop target features
      X = X.drop(["s1", "s2"], axis=1)

      #Apply Pairwise features
      X = pairwise_transform_features(X)

      #Convert to float
      X = X.astype(float)

      # Convert to tensors
      X_train = torch.tensor(X.values, dtype=torch.float32)

      #Optional Apply kernels

      return X_train

class CompatibilityModel(torch.nn.Module):
    #Simple binary classifcation model
    def __init__(self, d_features):
        super().__init__()
        self.W = torch.nn.Parameter(torch.randn(d_features, 1) * 0.01)

    def forward(self, X):
        return X @ self.W



def pairwise_transform_features(df):
    """
    Create interaction features between _1 and _2 columns:
    - sum
    - difference
    - division

    Returns a new DataFrame with appended columns.
    """

    df = df.copy()
    
    # Find shared base feature names (without _1 / _2 / metadata)
    base_features = sorted({
        col[:-2] for col in df.columns
        if col.endswith("_1") and col[:-2] + "_2" in df.columns and col[:-2] #not in skip_cols
    })

    #Create interactions between features for each base feature
    for feat in base_features:
        col1 = f"{feat}_1"
        col2 = f"{feat}_2"

        df[f"{feat}_sum"] = df[col1] + df[col2]
        df[f"{feat}_diff"] = df[col1] - df[col2]
        df[f"{feat}_div"] = df[col1] / (df[col2] + 1e-8)
    return df


#TRAIN FUNCTION
def train_model(lr=0.01, epochs=1000, track = True, shuffle = True, tol = 1e-7, graph =True, reg = 0.1):
    #read in data
    data = pd.read_csv("final_pairs.csv").drop(columns=["Unnamed: 0"], errors="ignore")

    #start pipeline
    pipeline = DataPrepPipeline()

    #Split data
    train_df, val_df = train_test_split(data, test_size=0.3,random_state=48,stratify=data["compatible"], shuffle = shuffle)


    # TRAIN DATA
    y_train = torch.tensor(train_df["compatible"].values, dtype=torch.float32).unsqueeze(1)
    X_train = pipeline.transform(train_df.drop(columns=["compatible"]))

    # VALIDATION DATA
    y_val = torch.tensor(val_df["compatible"].values, dtype=torch.float32).unsqueeze(1)
    X_val = pipeline.transform(val_df.drop(columns=["compatible"]))


    #TRAINING
    #Instantiate
    model = CompatibilityModel(X_train.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_fn = torch.nn.BCEWithLogitsLoss(reduction="mean")
    train_losses = []
    val_losses = []
    min_loss = float("inf")

    #Training loop
    for epoch in range(epochs):
        optimizer.zero_grad()

        #train loss
        logits = model(X_train)

        loss = loss_fn(logits, y_train)
        train_losses.append(loss.item())
        #validation loss
        with torch.no_grad(): 
          val_logits = model(X_val)
          val_loss = loss_fn(val_logits, y_val)
          val_losses.append(val_loss.item())
        #Saving best model on validation loss  
        if val_loss < min_loss:
          min_loss = val_loss
          print(val_loss)
          with open("model.pkl", "wb") as f:
            pickle.dump(model, f)


        #optimization step
        loss.backward()
        optimizer.step()

        #Check for convergence
        if epoch > 10:
            recent = val_losses[-5:]
            diffs = [abs(recent[i] - recent[i-1]) for i in range(1, len(recent))]
            if sum(diffs) / len(diffs) < tol:
                print(f"Converged at epoch {epoch}")
                break


  #Graphing
    if graph:
        graphLosses(train_losses, val_losses)
        # print("\nTraining Loss:", train_losses[-1])
        # print("Validation Loss:", val_losses[-1])

    #return model and validation data 
    return model, X_val, y_val

#Graphing function
def graphLosses(train_losses, val_losses):
  #Graphing the loss
  plt.figure(figsize=(8,5))
  plt.plot(train_losses, label="Train Loss")
  plt.plot(val_losses, label="Validation Loss")

  plt.xlabel("Epoch")
  plt.ylabel("Loss")
  plt.title("Training vs Validation Loss")
  plt.legend()
  plt.grid(True)

  # plt.gca().set_ylim(0,10)
  plt.show()

#evaluating model
def confusion_matrix(y_true, y_pred, n_classes=2):
    y_true = y_true.view(-1).long()
    y_pred = y_pred.view(-1).long()

    cm = torch.zeros((n_classes, n_classes), dtype=torch.int64)

    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1

    return cm