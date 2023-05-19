-- create matrix
CREATE OR REPLACE FUNCTION public.classe_music_by_name()
 RETURNS void
 LANGUAGE plpgsql
AS $function$
            BEGIN

                drop table if exists irish_music_classification_by_name;
                create table irish_music_classification_by_name (id_irish int,  path_son text, hornpipe int, strathspey int, waltz int, slipjig int, mazurka int, jig int, marche int, barndance int, polka int, reel int, slide int, song int); 
                insert into irish_music_classification_by_name (id_irish, path_son) select id_irish, path_son from irish2;
                update irish_music_classification_by_name set hornpipe=0, strathspey=0, waltz=0, slipjig=0, mazurka=0, jig=0, marche=0, barndance=0, polka=0, reel=0, slide=0, song=0;

                do
                $$
                declare r record;
                begin
                    for r in 
                    select danse, nom from danse_noms
                    loop
                    
                        if r.danse='reel' then raise notice 'ok';
                        end if;
                        if r.danse='reel' then update irish_music_classification_by_name set reel=reel+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='jig' then update irish_music_classification_by_name set jig=jig+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='hornpipe' then update irish_music_classification_by_name set hornpipe=hornpipe+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='marche' then update irish_music_classification_by_name set marche=marche+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='waltz' then update irish_music_classification_by_name set waltz=waltz+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='starthspey' then update irish_music_classification_by_name set strathspey=strathspey+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='slipjig' then update irish_music_classification_by_name set slipjig=slipjig+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='slide' then update irish_music_classification_by_name set slide=slide+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='polka' then update irish_music_classification_by_name set polka=polka+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='mazurka' then update irish_music_classification_by_name set mazurka=mazurka+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='barndance' then update irish_music_classification_by_name set barndance=barndance+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        elsif r.danse='song' then update irish_music_classification_by_name set song=song+1  where upper(path_son) LIKE '%'|| upper(r.nom) ||'%';
                        else raise notice '%', r.danse;
                        end if;

                    raise notice '% %', upper(r.danse), upper(r.nom);
                    end loop;
                end;
                $$;

            END;
            $function$
;



-- create dataset
CREATE OR REPLACE FUNCTION public.create_dataset()
 RETURNS TABLE(id integer, clas character varying)
 LANGUAGE plpgsql
AS $function$
        BEGIN
            drop table if exists train_dataset;
            create table train_dataset(id_irish int, classe VARCHAR(20));
            insert into train_dataset select id_irish, 'reel' as classe from irish_music_classification_by_name where reel>=3;
            insert into train_dataset select id_irish, 'jig' as classe from irish_music_classification_by_name where jig>=3;
            insert into train_dataset select id_irish, 'hornpipe' as classe from irish_music_classification_by_name where hornpipe>=2;
            insert into train_dataset select id_irish, 'polka' as classe from irish_music_classification_by_name where polka>=3;
            insert into train_dataset select id_irish, 'marche' as classe from irish_music_classification_by_name where marche>=2;
            insert into train_dataset select id_irish, 'slide' as classe from irish_music_classification_by_name where slide>=2;
            insert into train_dataset select id_irish, 'slipjig' as classe from irish_music_classification_by_name where slipjig>=2;
            insert into train_dataset select id_irish, 'strathspey' as classe from irish_music_classification_by_name where strathspey>=2;
            insert into train_dataset select id_irish, 'waltz' as classe from irish_music_classification_by_name where waltz>=2;
            insert into train_dataset select id_irish, 'mazurka' as classe from irish_music_classification_by_name where mazurka>=2;
            insert into train_dataset select id_irish, 'barndance' as classe from irish_music_classification_by_name where barndance>=2;
            insert into train_dataset select id_irish, 'song' as classe from irish_music_classification_by_name where song=1;
                        
            return query select id_irish, classe from train_dataset;
        --	drop table if exists train_dataset;
            
        END;
        $function$
;


-- TP, TN, FP, FN
CREATE OR REPLACE FUNCTION public.metrics()
 RETURNS TABLE(classifieur character varying, true_positives_song integer, true_negatives_song integer, false_postive_song integer, false_negative_song integer, accuracy integer, recall_song integer, precision_song integer, recall_instrumental integer, precision_instrumental integer)
 LANGUAGE plpgsql
AS $function$
begin
	
	drop table if exists c1;
	drop table if exists c2;
	drop table if exists c3;
	
	
	create table c1 as (
	with agg as(
		select count(id_irish) as tp, 'lstm' as classifieur from eval 
		where classe_lstm='song' and confirmation_classe='song'), 
	agg2 as (
		select count(id_irish) as tn, 'lstm' as classifieur from eval 
		where classe_lstm='nonsong' and confirmation_classe='nonsong'),
	agg3 as(
		select count(id_irish) as fp, 'lstm' as classifieur from eval 
		where classe_lstm='song' and confirmation_classe='nonsong'), 
	agg4 as (
		select count(id_irish) as fn, 'lstm' as classifieur from eval 
		where classe_lstm='nonsong' and confirmation_classe='song')
	select agg.classifieur,
		agg.tp, 
		agg2.tn, 
		agg3.fp, 
		agg4.fn 
		from agg 
		join agg2 on agg.classifieur=agg2.classifieur 
		join agg3 on agg.classifieur=agg3.classifieur
		join agg4 on agg.classifieur=agg4.classifieur);

	
	create table c2 as (
	with agg as(
		select count(id_irish) as tp, 'cnn' as classifieur from eval 
		where classe_cnn='song' and confirmation_classe='song'), 
	agg2 as (
		select count(id_irish) as tn, 'cnn' as classifieur from eval 
		where classe_cnn='nonsong' and confirmation_classe='nonsong'),
	agg3 as(
		select count(id_irish) as fp, 'cnn' as classifieur from eval 
		where classe_cnn='song' and confirmation_classe='nonsong'), 
	agg4 as (
		select count(id_irish) as fn, 'cnn' as classifieur from eval 
		where classe_cnn='nonsong' and confirmation_classe='song')
	select agg.classifieur,
		agg.tp, 
		agg2.tn, 
		agg3.fp, 
		agg4.fn 
		from agg 
		join agg2 on agg.classifieur=agg2.classifieur 
		join agg3 on agg.classifieur=agg3.classifieur
		join agg4 on agg.classifieur=agg4.classifieur);
	
	
	
	create table c3 as (
	with agg as(
		select count(id_irish) as tp, 'vgg' as classifieur from eval 
		where classe_vgg='song' and confirmation_classe='song'), 
	agg2 as (
		select count(id_irish) as tn, 'vgg' as classifieur from eval 
		where classe_vgg='nonsong' and confirmation_classe='nonsong'),
	agg3 as(
		select count(id_irish) as fp, 'vgg' as classifieur from eval 
		where classe_vgg='song' and confirmation_classe='nonsong'), 
	agg4 as (
		select count(id_irish) as fn, 'vgg' as classifieur from eval 
		where classe_vgg='nonsong' and confirmation_classe='song')
	select agg.classifieur,
		agg.tp, 
		agg2.tn, 
		agg3.fp, 
		agg4.fn 
		from agg 
		join agg2 on agg.classifieur=agg2.classifieur 
		join agg3 on agg.classifieur=agg3.classifieur
		join agg4 on agg.classifieur=agg4.classifieur);

	
	
	return query
	with agg as(
	select c1.*, 'lstm' as typ from c1 
	union all
	select c2.*, 'cnn' as typ from c2 
	union all 
	select c3.*, 'vgg' as typ from c3
	)
	select typ::VARCHAR(4),
		((tp::float)/4)::int, 
		((tn::float)/4)::int, 
		((fp::float)/4)::int, 
		((fn::float)/4)::int,
		((tp+tn)/(400.0)*100)::int as acc0,
		((tp)/(tp+fn)::float*100)::int as rec0,
		((tp)/(tp+fp)::float*100)::int as prec0,
		((tn)/(tn+fp)::float*100)::int as rec1,
		((tn)/(tn+fn)::float*100)::int as prec1
		from agg;
	
	drop table if exists c1;
	drop table if exists c2;
	drop table if exists c3;
	


end;
$function$
;



-- create dataset 2
CREATE OR REPLACE FUNCTION public.random_choice()
 RETURNS void
 LANGUAGE plpgsql
AS $function$
begin 
	
	drop table if exists rand_classes;

	create table rand_classes(
		id_irish int,
		classe varchar(20),
		confirmation_classe varchar(20) 
		);
	
	insert into rand_classes(id_irish, classe) 
			with agg as(
			select 
			id_irish,
			case when vgg<0.5 then 'song' else 'nonsong' end as classe
			from irish2
			where labelised!=1
		)
		select id_irish, classe from agg
		where classe='song' order by random() limit 100;

	insert into rand_classes(id_irish, classe)	
		with agg as(
			select 
			id_irish,
			case when vgg<0.5 then 'song' else 'nonsong' end as classe
			from irish2
			where labelised!=1
		)
		select id_irish, classe from agg
		where classe='nonsong' order by random() limit 100;
	
	
end; $function$
;



-- utilitaire 1
CREATE OR REPLACE VIEW public.repartition_danses
AS WITH agg AS (
         SELECT create_dataset.id,
            create_dataset.clas AS danse
           FROM create_dataset() create_dataset(id, clas)
        )
 SELECT agg.danse,
    count(agg.danse) AS count
   FROM agg
  GROUP BY agg.danse
  ORDER BY (count(agg.danse)) DESC;



-- utilitaire 2 
CREATE OR REPLACE VIEW public.repartition_danses_par_dossier
AS WITH agg AS (
         SELECT create_dataset.id,
            create_dataset.clas AS danse
           FROM create_dataset() create_dataset(id, clas)
        )
 SELECT split_part(irish2.path_son, '/'::text, 2) AS dossier,
    count(agg.danse) AS "airs_labellisés_par_dossier"
   FROM agg
     LEFT JOIN irish2 ON irish2.id_irish = agg.id
  GROUP BY (split_part(irish2.path_son, '/'::text, 2))
  ORDER BY (count(agg.danse)) DESC;