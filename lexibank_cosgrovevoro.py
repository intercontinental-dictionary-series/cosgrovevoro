import pathlib

import pylexibank
from idspy import IDSDataset, IDSEntry


class Dataset(IDSDataset):
    dir = pathlib.Path(__file__).parent
    id = "cosgrovevoro"

    def cmd_download(self, args):
        self.raw_dir.xls2csv("ids_voro1241.xlsx")

    def cmd_makecldf(self, args):
        glottocode = "voro1241"
        reprs = ["StandardOrth"]

        args.writer.add_concepts(id_factory=lambda c: c.attributes['ids_id'])
        args.writer.add_sources(*self.raw_dir.read_bib())

        personnel = self.get_personnel(args)

        args.writer.add_language(
            ID=glottocode,
            Name="Võro",
            Glottocode=glottocode,
            Authors=personnel['author'],
            DataEntry=personnel['data entry'],
            Consultants=personnel['consultant'],
            Representations=reprs,
            Latitude=58.0,
            Longitude=26.6,
            date='2020-09-17',
        )

        for form in pylexibank.progressbar(self.read_csv("ids_voro1241.idsclldorg.csv")):
            if form.form:
                args.writer.add_lexemes(
                    Language_ID=glottocode,
                    Parameter_ID=form.ids_id,
                    Value=form.form,
                    Comment=form.comment,
                    Source="cosgrove2020",
                    Transcriptions=reprs,
                )

        self.apply_cldf_defaults(args)

    def entry_from_row(self, row):
        return IDSEntry("%s-%s" % (row[0], row[1]), ";".join(filter(None, row[3:10])), "", "")
