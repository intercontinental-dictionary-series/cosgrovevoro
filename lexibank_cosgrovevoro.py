import attr
from clldutils.path import Path
import pylexibank


@attr.s
class IDSLexeme(pylexibank.Lexeme):
    Transcription = attr.ib(default=None)
    AlternativeValue = attr.ib(default=None)
    AlternativeTranscription = attr.ib(default=None)


@attr.s
class IDSLanguage(pylexibank.Language):
    Contributors = attr.ib(default=None)
    default_representation = attr.ib(default=None)
    alt_representation = attr.ib(default=None)
    alt_names = attr.ib(default=None)
    date = attr.ib(default=None)


class IDSEntry:
    def __init__(self, ids_id, form, alt_form, comment):
        self.ids_id = ids_id
        self.form = form
        self.alt_form = alt_form
        self.comment = comment


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "cosgrovevoro"

    lexeme_class = IDSLexeme
    language_class = IDSLanguage

    form_spec = pylexibank.FormSpec(
        brackets={"(": ")"},
        separators=";",
        missing_data=('?', '-'),
        strip_inside_brackets=False
    )

    def cmd_download(self, args):
        self.raw_dir.xls2csv("ids_cl_võro.xlsx")

    def cmd_makecldf(self, args):
        glottocode = "voro1241"
        lang_id = glottocode
        lang_name = "Võro"
        transcription = "StandardOrth"
        source = "cosgrove2020"

        ccode = {
            x.attributes["ids_id"]:
                {
                    "concepticon_id": x.concepticon_id,
                    "concepticon_gloss": x.concepticon_gloss,
                    "name": x.english,
                }
                for x in self.conceptlists[0].concepts.values()
        }

        args.writer.add_sources(*self.raw_dir.read_bib())

        args.writer.add_language(
            ID=lang_id,
            Name=lang_name,
            Glottocode=glottocode,
            Contributors=['Leon Cosgrove|Author', 'Sulev Iva|Author', 'Leon Cosgrove|Data Entry'],
            default_representation=transcription,
            date='2020-09-17',
        )

        # add data
        for form in pylexibank.progressbar(self.read_csv()):
            args.writer.add_concept(
                ID=form.ids_id,
                Name=ccode[form.ids_id]["name"],
                Concepticon_ID=ccode[form.ids_id]["concepticon_id"],
                Concepticon_Gloss=ccode[form.ids_id]["concepticon_gloss"],
            )
            if form.form:
                args.writer.add_lexemes(
                    Language_ID=lang_id,
                    Parameter_ID=form.ids_id,
                    Value=form.form,
                    Comment=form.comment,
                    Source=source,
                    Transcription=transcription,
                )

        args.writer.cldf['LanguageTable', 'Contributors'].separator = ";"
        args.writer.cldf['LanguageTable', 'alt_names'].separator = ";"

    def read_csv(self, fname="ids_cl_võro.idsclldorg.csv"):
        try:
            for i, row in enumerate(self.raw_dir.read_csv(fname)):
                row = [c.strip() for c in row[0:10]]
                if i > 0:
                    row[0:2] = [int(float(c)) for c in row[0:2]]
                    entry = IDSEntry(
                        "%s-%s" % (row[0], row[1]),
                        ";".join(filter(None, row[3:10])),
                        "",
                        ""
                    )
                    yield entry
        except Exception as e:
            print(e)
            print("Execute 'download %s' first?" % (self.id))
