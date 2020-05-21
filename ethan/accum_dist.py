def calc_accum_dist(data):
    try:
        accums = []
        issss = []
        accums_stdv = []

        tops = []

        prev = 0
        counter = 0
        for index, row in data.iterrows():
            i_date = datetime.datetime.strptime(index, "%Y-%m-%d %H:%M:00")
            if i_date <= get_past_date(datetime.datetime.now(), 5):
                continue

            o = row['1. open']
            c = row['4. close']
            h = row['2. high']
            l = row['3. low']
            v = row['5. volume']

            numer = round((o - c), 2)
            denom = round((h - l), 2)


            reatio_vol = 0
            if numer == 0 or denom == 0:
                reatio_vol = v
            else:
                ratio = numer / denom
                reatio_vol = (ratio * v) * -1

            accum = reatio_vol + prev
            prev = accum

            issss.append(index)
            accums.append(accum)
            counter += 1

            if counter > 12:
                accums_stdv.append(statistics.stdev(accums[-12:]))


            # if counter > 25:
            #     if is_accum_top(accums_stdv[-5:]):
            #         tops.append((list(accums_stdv[-3:-2])[0], counter))

        # print "tops", tops


        # accums_stdv_mean = statistics.mean(accums_stdv) * 3
        # final_tops = list(filter(lambda x: x[0] > accums_stdv_mean, tops))
        # # tops_idx = list(map(lambda x: accums_stdv.index(x), final_tops))


        # print "final_tops", final_tops
        # # print "tops_idx", tops_idx




        # final_tops = [(statistics.mean(accums_stdv)) for i in tops]
        # statistics.mean(accums_stdv)
        return { 'accumdist': accums[-1], 'accumdist_stdv': accums_stdv[-1],
                'accumdist_total': accums, 'accumdist_stdv_total': accums_stdv, 
                'accum_tops': tops, 'aa': 'aa',}
    except Exception, e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname  = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print "ticker!!!: ", exc_type, fname, exc_tb.tb_lineno
        # return { 'accumdist': 0, 'accumdist_stdv': 0}
        pass
        # print e
        # raise e
