if __name__ == '__main__':

    intpufile = open("./NIADic.csv", mode="r", encoding="utf-8")
    # intpufile = open("./in.txt", mode="r", encoding="utf-8")
    outfile = open("./out.txt", mode="w", encoding="utf-8")

    singleKoList = ["ㅂ", "ㅃ", "ㅈ", "ㅉ", "ㄷ", "ㄸ", "ㄱ", "ㄲ", "ㅅ", "ㅆ", "ㅛ", "ㅕ", "ㅑ", "ㅒ", "ㅐ", "ㅁ", "ㄴ", "ㅇ", "ㄹ", "ㅎ",
                    "ㅗ", "ㅓ", "ㅏ", "ㅣ", "ㅋ", "ㅌ", "ㅊ", "ㅍ", "ㅠ", "ㅜ", "ㅡ", "ㆎ", "ㆎ"
        , "ㆍ"
        , "ㆌ"
        , "ㆊ"
        , "ㆉ"
        , "ㆅ"
        , "ㅢ"
        , "ㅟ"
        , "ㅞ"
        , "ㅝ"
        , "ㅚ"
        , "ㅙ"
        , "ㅘ"
        , "ㅖ"
        , "ㅔ"
        , "□"
        , "ㅭ"
        , "ㆁ"]
    lines = intpufile.readlines()
    for idx, line in enumerate(lines):
        line = line.strip()
        next_flag = 0
        for singleKo in singleKoList:
            if line.count(singleKo) > 0:
                next_flag = 1
                break

        line_split = line.split(",")
        print(line_split)
        if next_flag == 0 and len(line) > 1 and int(line_split[-1]) > 1 and len(line_split) == 4:


                print(line)
                outfile.writelines(str(line) + "\n")

                outfile_tag = open("./jjeaby_"+line_split[1]+".txt", mode="a", encoding="utf-8")
                outfile_tag.writelines(line_split[0]+ "\n")
                outfile_tag.close()


    outfile.close()
    # keys = mdx_builder.get_mdx_keys()
    # keys1 = mdx_builder.get_mdx_keys('abstrac')
    # keys2 = mdx_builder.get_mdx_keys('*tion')
    # for key in keys2:
    # text = mdx_builder.mdx_lookup(key)[0]
