int init_predictor(const char *model_path)
{
    ort = OrtGetApiBase()->GetApi(ORT_API_VERSION);
    if (!ort) { fprintf(stderr, "Could not get ORT API\n"); return -1; }

    /* 1.  environment */
    ORTCHK( ort->CreateEnv(ORT_LOGGING_LEVEL_WARNING,
                           "levelshift", &env) );

    /* 2.  session options */
    OrtSessionOptions *opts = NULL;
    ORTCHK( ort->CreateSessionOptions(&opts) );
    ort->SetIntraOpNumThreads(opts, 1);   // no per-core pinning
    ort->SetInterOpNumThreads(opts, 1);   // optional, keeps things single-threaded
    ORTCHK( ort->SetSessionGraphOptimizationLevel(opts,
                                                  ORT_ENABLE_BASIC) );

    /* 3.  session */
    printf("Loading ONNX model: %s\n", model_path);
    ORTCHK( ort->CreateSession(env, model_path, opts, &sess) );
    ort->ReleaseSessionOptions(opts);

    /* 4.  CPU memory info handle */
    ORTCHK( ort->CreateCpuMemoryInfo(OrtDeviceAllocator,
                                     OrtMemTypeDefault, &memcpu) );

    return 0;           /* success */
}
static void _check(OrtStatus *st, const char *msg)
{
    if (!st) return;
    fprintf(stderr, "ORT-ERROR %s: %s\n", msg, ort->GetErrorMessage(st));
    abort();                                 /* stop instead of seg-fault */
}

float predict_levelshift_prob(const float feats[6]) /* Using the default model that takes 6 input features */
{
    const int64_t shape[2] = {1, 6};
    OrtValue *x   = NULL;
    OrtValue *out = NULL;

    _check(ort->CreateTensorWithDataAsOrtValue(
               memcpu, (void*)feats, 6*sizeof(float),
               shape, 2, ONNX_TENSOR_ELEMENT_DATA_TYPE_FLOAT, &x),
           "create tensor");

    const char *in_names[]  = {"x"};
    const char *out_names[] = {"probabilities"};   /* adjust if needed */

    _check(ort->Run(sess, NULL,
                    in_names,  &x,   1,
                    out_names, 1,    &out),
           "OrtRun");

    float *p = NULL;
    _check(ort->GetTensorMutableData(out, (void**)&p), "mutable data");

    float prob = p[1];
    ort->ReleaseValue(out);
    ort->ReleaseValue(x);
    return prob;
}

void free_predictor(void)
{
    ort->ReleaseMemoryInfo(memcpu);
    ort->ReleaseSession(sess);
    ort->ReleaseEnv(env);
}